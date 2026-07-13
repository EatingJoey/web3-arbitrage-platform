package core

import (
	"math"
	"math/big"
)

func CalculatePrice(sqrtPriceX96 *big.Int) float64 {
	spx := new(big.Int).Set(sqrtPriceX96)
	spx2 := new(big.Int).Mul(spx, spx)

	// 2. 除以 2^192 得到原始价格
	Q192 := new(big.Int).Lsh(big.NewInt(1), 192)
	price := new(big.Float).SetInt(spx2)
	denom := new(big.Float).SetInt(Q192)
	price.Quo(price, denom)

	// 3. 取倒数，得到 ETH 价格
	one := new(big.Float).SetFloat64(1.0)
	price.Quo(one, price)

	// 4. 放大精度（关键！！！）
	scale := new(big.Float).SetFloat64(1000000000000.0)
	price.Mul(price, scale)

	// 输出
	f, _ := price.Float64()
	return f
}

func CalculatePriceV3(
	sqrtPriceX96 *big.Int,
	token0Decimals int,
	token1Decimals int,
	reverse bool,
) float64 {

	// sqrtPrice / 2^96
	sqrt := new(big.Float).SetInt(sqrtPriceX96)

	q96 := new(big.Float).SetFloat64(math.Pow(2, 96))
	ratio := new(big.Float).Quo(sqrt, q96)

	// square => price token1/token0
	price := new(big.Float).Mul(ratio, ratio)

	// decimals correction
	diff := token0Decimals - token1Decimals
	scale := math.Pow(10, float64(diff))

	p, _ := price.Float64()
	p *= scale

	// 是否反向
	if reverse {
		p = 1.0 / p
	}

	return p
}
