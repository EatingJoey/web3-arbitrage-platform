package rpc

import (
	"log"
	"web3bot/config"

	"github.com/ethereum/go-ethereum/ethclient"
)

var Client *ethclient.Client

func Init() {
	var err error
	Client, err = ethclient.Dial(config.RPCUrl)
	if err != nil {
		log.Fatalf("rpc dial: %v", err)
	}
	log.Println("✅ eth client initialized")
}
