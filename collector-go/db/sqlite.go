package db

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

type ChainEvent struct {
	gorm.Model
	TxHash      string `gorm:"uniqueIndex;size:100"`
	BlockNumber uint64
	Amount      string
	EventTime   int64
	EventName   string
}

func InitDB() error {
	var err error
	DB, err = gorm.Open(sqlite.Open("chain.db?_journal=WAL"), &gorm.Config{})
	if err != nil {
		return err
	}
	return DB.AutoMigrate(&ChainEvent{})
}
