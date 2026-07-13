package main

import (
	"web3bot/api"
	"web3bot/cache"
	"web3bot/db"

	//"web3bot/service"
	"log"
	"sync"
	"time"
	"web3bot/config"
	"web3bot/core"
	"web3bot/rpc"
)

var lastSentPrice float64 = 0

func main() {
	// 初始化 RPC
	config.Init()
	rpc.Init()
	log.Println("🚀 WEB3 ARB BOT - PRO MULTI-POOL MODE")

	// 加载所有池子配置
	pools := config.LoadPools()
	if len(pools) == 0 {
		log.Fatal("❌ 未配置任何交易池子")
	}

	log.Printf("✅ 成功加载 %d 个池子", len(pools))

	db.InitDB()
	// 启动 API 服务
	go api.Start()
	// 并发监听所有池子
	var wg sync.WaitGroup
	for _, pool := range pools {
		wg.Add(1)
		// 每个池子独立协程，生产级并发模型
		go func(p config.PoolConfig) {
			defer wg.Done()
			runPoolLoop(p)
		}(pool)
	}

	select {}

}

// 单池子独立循环
func runPoolLoop(pool config.PoolConfig) {
	//var lastSentPrice float64 = 0
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	log.Printf("[%s] 开始监控池子", pool.Name)

	for range ticker.C {
		// 1. 获取当前池子价格
		//price := core.GetPoolPrice(pool.PoolAddress)
		price := core.GetPoolPriceV3(pool.PoolAddress, pool.Token0Decimals, pool.Token1Decimals, pool.Reverse)
		if price <= 0 {
			continue
		}
		log.Printf("[%s] 当前价格: %f", pool.Name, price)

		cache.PriceCache.Store(
			pool.Name,
			cache.PriceInfo{
				Pool:      pool.Name,
				Price:     price,
				Timestamp: time.Now().Unix()})

		// 2. 策略价格计算
		// if lastSentPrice == 0 {
		// 	lastSentPrice = price
		// } else {
		// 	lastSentPrice += 100.0
		// }

		// 3. 策略判断
		// if strategy.ShouldTrade(pool, lastSentPrice) {
		// 	log.Printf("[%s] 🔥 触发交易", pool.Name)
		// 	tx, err := core.Trade(pool)
		// 	if err != nil {
		// 		log.Printf("[%s] ❌ 交易失败: %v", pool.Name, err)
		// 	} else {
		// 		log.Printf("[%s] ✅ 交易成功: %s", pool.Name, tx.Hex())
		// 	}
		// }
	}
}
