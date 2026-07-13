package api

import (
	"net/http"
	"web3bot/cache"
	"web3bot/db"

	"github.com/gin-gonic/gin"
)

func Start() {
	r := gin.Default()

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "running"})
	})

	r.GET("/events", func(c *gin.Context) {
		var list []db.ChainEvent
		db.DB.Order("id desc").Limit(20).Find(&list)
		c.JSON(http.StatusOK, list)
	})

	r.GET("/swapevents", func(c *gin.Context) {
		var list []db.SwapLog
		db.DB.Order("id desc").Limit(20).Find(&list)
		c.JSON(http.StatusOK, list)
	})

	r.GET("/prices", func(c *gin.Context) {
		result := make([]cache.PriceInfo, 0)
		cache.PriceCache.Range(func(_, value any) bool {
			result = append(
				result,
				value.(cache.PriceInfo),
			)
			return true
		})
		c.JSON(200, result)
	})
	r.Run(":8080")
}
