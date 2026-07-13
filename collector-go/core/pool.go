package core

import (
	"context"
	"log"
	"math/big"
	"web3bot/rpc"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
)

func GetPoolPrice(poolAddr common.Address) float64 {
	if rpc.Client == nil {
		log.Println("❌ RPC 未初始化")
		return 0
	}

	var result hexutil.Bytes
	data := "0x3850c7bd"

	err := rpc.Client.Client().CallContext(context.Background(), &result,
		"eth_call",
		map[string]any{
			"to":   poolAddr.Hex(),
			"data": data,
		},
		"latest",
	)

	if err != nil {
		log.Printf("[%s] 调用失败: %v", poolAddr.Hex(), err)
		return 0
	}

	res := []byte(result)
	if len(res) < 32 {
		return 0
	}

	sqrt := new(big.Int).SetBytes(res[:32])
	return CalculatePrice(sqrt)
}

func GetPoolPriceV3(poolAddr common.Address, Token0Decimals int, Token1Decimals int, Reverse bool) float64 {
	if rpc.Client == nil {
		log.Println("❌ RPC 未初始化")
		return 0
	}
	var result hexutil.Bytes
	err := rpc.Client.Client().CallContext(
		context.Background(),
		&result,
		"eth_call",
		map[string]any{
			"to":   poolAddr.Hex(),
			"data": "0x3850c7bd",
		},
		"latest")

	if err != nil {
		log.Printf("[%s] 调用失败: %v", poolAddr.Hex(), err)
		return 0
	}

	if len(result) < 32 {
		return 0
	}

	sqrt := new(big.Int).SetBytes(result[0:32])

	price := CalculatePriceV3(
		sqrt,
		Token0Decimals,
		Token1Decimals,
		Reverse)

	return price
}
