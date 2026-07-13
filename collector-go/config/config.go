package config

import (
	"os"

	"github.com/ethereum/go-ethereum/common"
	"github.com/joho/godotenv"
)

type PoolConfig struct {
	Name           string         // 池子名称：ETH/USDC
	PoolAddress    common.Address // 池子合约地址
	RouterAddr     common.Address // 路由地址
	Token0         common.Address
	Token1         common.Address
	FeeTier        uint32
	AmountIn       string
	GasLimit       uint64
	Token0Decimals int
	Token1Decimals int
	Reverse        bool
}

func Init() {
	_ = godotenv.Load("../.env")
	PK = os.Getenv("PK")
	RPCUrl = os.Getenv("RPCUrl")
}

var (
	GasLimit = uint64(1500000)
	PK       string
	RPCUrl   string
)

// var (
// 	RPC            = "wss://sepolia.infura.io/ws/v3/4ec7a4f8f43f46e5b51175ff9edbe57f"
// 	PythonAddr     = "http://127.0.0.1:8000/strategy"
// 	Contract       = "0x78B691Fac809bF8Df3Fd6E1B70c11b15Ca9934AB"
// 	StartBlock     = uint64(10560000)
// 	RouterAddr     = common.HexToAddress("0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E")
// 	PoolAddr       = common.HexToAddress("0x3289680dd4d6c10bb19b899729cda5eef58aeff1")
// 	Token0         = common.HexToAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14") // WETH
// 	Token1         = common.HexToAddress("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238") // USDC
// 	AmountIn       = "10000000000000000"                                               // 0.01 ETH
// 	FeeTier        = uint32(3000)
// 	SepoliaUNIV2WU = "0x3289680dd4d6c10bb19b899729cda5eef58aeff1" // Sepolia UNIV2 WETH/USDC
// )

// 生产环境：多池子配置
func LoadPools() []PoolConfig {
	return []PoolConfig{
		// {
		// 	Name:        "ETH-USDC-500",
		// 	PoolAddress: common.HexToAddress("0x3289680dd4d6c10bb19b899729cda5eef58aeff1"),
		// 	RouterAddr:  common.HexToAddress("0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E"),
		// 	Token0:      common.HexToAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14"),
		// 	Token1:      common.HexToAddress("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"),
		// 	FeeTier:     uint32(500),
		// 	AmountIn:    "10000000000000000",
		// 	GasLimit:    uint64(1500000),
		// },
		// 👇 可以无限加池子
		// {
		// 	Name:        "BTC-USDT-3000",
		// 	PoolAddress: common.HexToAddress("0x6418eec70f50913ff0d756b48d32ce7c02b47c47"),
		// 	RouterAddr:  common.HexToAddress("0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E"),
		// 	Token0:      common.HexToAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14"),
		// 	Token1:      common.HexToAddress("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"),
		// 	FeeTier:     uint32(3000),
		// 	AmountIn:    "10000000000000000",
		// 	GasLimit:    uint64(1500000),
		// },
		// {
		// 	Name:        "BTC-USDT-4000",
		// 	PoolAddress: common.HexToAddress("0x6ce0896eae6d4bd668fde41bb784548fb8f59b50"),
		// 	RouterAddr:  common.HexToAddress("0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E"),
		// 	Token0:      common.HexToAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14"),
		// 	Token1:      common.HexToAddress("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"),
		// 	FeeTier:     uint32(4000),
		// 	AmountIn:    "10000000000000000",
		// 	GasLimit:    uint64(1500000),
		// },
		// {
		// 	Name:        "WETH-USDC",
		// 	PoolAddress: common.HexToAddress("0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"),
		// 	RouterAddr:  common.HexToAddress("0x3bFA4769FB09eefC5a80d6E87c3B9C650f7Ae48E"),
		// 	Token0:      common.HexToAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14"),
		// 	Token1:      common.HexToAddress("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"),
		// 	FeeTier:     uint32(4000),
		// 	AmountIn:    "10000000000000000",
		// 	GasLimit:    uint64(1500000),
		// },
		{
			Name:           "WBTC-USDC",
			PoolAddress:    common.HexToAddress("0x99ac8ca7087fa4a2a1fb6357269965a2014abc35"),
			Token0Decimals: 8,
			Token1Decimals: 6,
			FeeTier:        uint32(4000),
			AmountIn:       "10000000000000000",
			GasLimit:       uint64(1500000),
			Reverse:        false,
		},
	}
}
