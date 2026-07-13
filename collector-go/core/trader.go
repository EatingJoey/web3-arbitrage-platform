package core

import (
	"context"
	"math/big"
	"os"
	"strings"
	"time"
	"web3bot/config"
	"web3bot/rpc"

	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
)

// 多池子交易
func Trade(pool config.PoolConfig) (common.Hash, error) {
	pk, err := crypto.HexToECDSA(config.PK)
	if err != nil {
		return common.Hash{}, err
	}

	chainID, err := rpc.Client.ChainID(context.Background())
	if err != nil {
		return common.Hash{}, err
	}

	auth, err := bind.NewKeyedTransactorWithChainID(pk, chainID)
	if err != nil {
		return common.Hash{}, err
	}

	gasPrice, _ := rpc.Client.SuggestGasPrice(context.Background())
	auth.GasPrice = gasPrice
	auth.GasLimit = pool.GasLimit

	file, err := os.ReadFile("abi/Router.abi.json")
	if err != nil {
		return common.Hash{}, err
	}
	routerABI, _ := abi.JSON(strings.NewReader(string(file)))

	amountIn, _ := new(big.Int).SetString(pool.AmountIn, 10)
	args := []interface{}{
		pool.Token0,
		pool.Token1,
		big.NewInt(int64(pool.FeeTier)),
		auth.From,
		big.NewInt(time.Now().Unix() + 120),
		amountIn,
		big.NewInt(0),
		big.NewInt(0),
	}

	input, _ := routerABI.Pack("exactInputSingle", args...)
	nonce, _ := rpc.Client.PendingNonceAt(context.Background(), auth.From)

	tx := types.NewTransaction(nonce, pool.RouterAddr, big.NewInt(0), auth.GasLimit, auth.GasPrice, input)
	signedTx, _ := auth.Signer(auth.From, tx)

	if err := rpc.Client.SendTransaction(context.Background(), signedTx); err != nil {
		return common.Hash{}, err
	}

	return signedTx.Hash(), nil
}
