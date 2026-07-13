package service

import (
	"context"
	"math/big"
	"os"
	"os/signal"
	"syscall"
	"time"
	"web3bot/config"
	"web3bot/db"

	"github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

// ===================== Uniswap V3 Swap 事件 Topic =====================
var swapTopic = common.HexToHash("0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67")

// ===================== ABI =====================
// V3 不需要 ABI！直接解析 Data，所以我直接删掉 ABI 相关代码！

// ===================== 全局 client =====================
var client *ethclient.Client // 全局

// ===================== init 初始化 =====================
func init() {
	zerolog.TimeFieldFormat = time.RFC3339
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	log.Info().Msg("✅ Uniswap V3 监听模块初始化完成")
}

// ===================== 启动监听 =====================
func StartListenUniswap() {
	// ✅ 这里必须用 = 不要用 := ！！！！！
	var err error
	client, err = ethclient.Dial(config.RPC) // 全局赋值
	if err != nil {
		log.Fatal().Err(err).Msg("RPC 连接失败")
	}
	log.Info().Msg("✅ 已连接链节点")

	poolAddr := common.HexToAddress(config.SepoliaUNIV2WU)
	lastProcessedBlock := uint64(0)

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	log.Info().Msg("🚀 Uniswap V3 量化监听（轮询模式）启动")

	for {
		select {
		case <-sigCh:
			log.Info().Msg("🛑 程序退出")
			return
		default:
			header, err := client.HeaderByNumber(context.Background(), nil)
			if err != nil {
				log.Error().Err(err).Msg("获取区块失败")
				time.Sleep(3 * time.Second)
				continue
			}
			currentBlock := header.Number.Uint64()

			if lastProcessedBlock == 0 {
				lastProcessedBlock = currentBlock - 10
			}

			if currentBlock <= lastProcessedBlock {
				time.Sleep(2 * time.Second)
				continue
			}

			query := ethereum.FilterQuery{
				FromBlock: big.NewInt(int64(lastProcessedBlock)),
				ToBlock:   big.NewInt(int64(currentBlock)),
				Addresses: []common.Address{poolAddr},
				Topics:    [][]common.Hash{{swapTopic}},
			}

			logs, err := client.FilterLogs(context.Background(), query)
			if err != nil {
				log.Error().Err(err).Msg("FilterLogs 失败")
				time.Sleep(3 * time.Second)
				continue
			}

			// 🔥 这里一旦抓到，马上打印！
			if len(logs) > 0 {
				log.Info().Int("count", len(logs)).Msg("🔥 抓到 Swap 事件！")
			}

			for _, vLog := range logs {
				handleSwap(vLog) // 同步处理，避免并发丢日志
			}

			lastProcessedBlock = currentBlock
			log.Info().Uint64("last_block", lastProcessedBlock).Msg("区块扫描完成")
			time.Sleep(1 * time.Second)
		}
	}
}

// ===================== V3 Swap 处理（100% 正确） =====================
func handleSwap(vLog types.Log) {
	// V3 不需要 ABI！直接解析
	if len(vLog.Topics) < 3 {
		log.Error().Msg("topic 长度不够")
		return
	}

	sender := common.HexToAddress(vLog.Topics[1].Hex())
	recipient := common.HexToAddress(vLog.Topics[2].Hex())

	amount0 := new(big.Int).SetBytes(vLog.Data[:32])
	amount1 := new(big.Int).SetBytes(vLog.Data[32:64])
	sqrtPriceX96 := new(big.Int).SetBytes(vLog.Data[64:96])
	liquidity := new(big.Int).SetBytes(vLog.Data[96:128])

	price := calculateV3Price(sqrtPriceX96)

	record := db.SwapLog{
		TxHash:      vLog.TxHash.Hex(),
		Sender:      sender.Hex(),
		ToAddr:      recipient.Hex(),
		Amount0In:   amount0.String(),
		Amount1In:   amount1.String(),
		Amount0Out:  "0",
		Amount1Out:  "0",
		Reserve0:    "0",
		Reserve1:    liquidity.String(),
		Price:       price,
		BlockNumber: vLog.BlockNumber,
	}

	if err := db.DB.Create(&record).Error; err != nil {
		log.Error().Err(err).Msg("入库失败")
		return
	}

	log.Info().
		Str("tx", vLog.TxHash.Hex()[:10]).
		Str("price", price).
		Uint64("block", vLog.BlockNumber).
		Msg("✅ 捕获 V3 Swap → 已入库")
}

// ===================== V3 价格计算 =====================
func calculateV3Price(sqrtPriceX96 *big.Int) string {
	sqrtPrice := new(big.Float).SetInt(sqrtPriceX96)
	twoPow96 := new(big.Float).SetInt(new(big.Int).Lsh(big.NewInt(1), 96))
	price := new(big.Float).Quo(sqrtPrice, twoPow96)
	price = new(big.Float).Mul(price, price)
	return price.Text('f', 6)
}
