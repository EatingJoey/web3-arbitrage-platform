package strategy

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"web3bot/config"
)

func ShouldTrade(pool config.PoolConfig, price float64) bool {
	url := "http://127.0.0.1:8000/strategy"

	body := map[string]interface{}{
		"pool":  pool.Name,
		"price": price,
	}

	jsonData, _ := json.Marshal(body)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Printf("[%s] 策略调用失败", pool.Name)
		return false
	}
	defer resp.Body.Close()

	var res map[string]bool
	_ = json.NewDecoder(resp.Body).Decode(&res)
	return res["trade"]
}
