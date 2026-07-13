package service

import (
	"context"
	"log"
	"math/big"
	"os"
	"strings"
	"time"
	"web3bot/config"
	"web3bot/db"

	"github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
)

var contractABI abi.ABI
var lastProcessedBlock uint64 = config.StartBlock

func init() {
	file, err := os.ReadFile("abi/Lock.abi.json")
	if err != nil {
		log.Fatalf("ABI 加载失败: %v", err)
	}
	contractABI, err = abi.JSON(strings.NewReader(string(file)))
	if err != nil {
		log.Fatalf("ABI 解析失败: %v", err)
	}
}

// 企业级 WSS 轮询监听（你自己的 INFURA 完美支持）
func StartListener() {
	log.Println("✅ 企业级公链监听启动 (Sepolia WSS)")

	client, err := ethclient.Dial(config.RPC)
	if err != nil {
		log.Fatalf("RPC 连接失败: %v", err)
	}

	for {
		header, err := client.HeaderByNumber(context.Background(), nil)
		if err != nil {
			log.Printf("获取区块失败，3秒后重试: %v", err)
			time.Sleep(3 * time.Second)
			continue
		}

		currentBlock := header.Number.Uint64()
		if currentBlock <= lastProcessedBlock {
			time.Sleep(2 * time.Second)
			continue
		}

		query := ethereum.FilterQuery{
			FromBlock: big.NewInt(int64(lastProcessedBlock)),
			ToBlock:   big.NewInt(int64(currentBlock)),
			Addresses: []common.Address{common.HexToAddress(config.Contract)},
		}

		logs, err := client.FilterLogs(context.Background(), query)
		if err == nil {
			for _, logObj := range logs {
				parseEvent(logObj)
			}
		}

		lastProcessedBlock = currentBlock
		time.Sleep(1 * time.Second)
	}
}

func parseEvent(logObj types.Log) {
	txHash := logObj.TxHash.Hex()

	var count int64
	db.DB.Model(&db.ChainEvent{}).Where("tx_hash = ?", txHash).Count(&count)
	if count > 0 {
		return
	}

	type WithdrawalEvent struct {
		Amount *big.Int
		When   *big.Int
	}

	var event WithdrawalEvent
	if err := contractABI.UnpackIntoInterface(&event, "Withdrawal", logObj.Data); err != nil {
		return
	}

	db.DB.Create(&db.ChainEvent{
		TxHash:      txHash,
		BlockNumber: logObj.BlockNumber,
		Amount:      event.Amount.String(),
		EventTime:   event.When.Int64(),
		EventName:   "Withdrawal",
	})

	ethValue := new(big.Float).Quo(new(big.Float).SetInt(event.Amount), new(big.Float).SetInt(big.NewInt(1e18)))
	log.Printf("📦 成功监听提款 | Tx: %s | %.6f ETH", txHash, ethValue)
}
