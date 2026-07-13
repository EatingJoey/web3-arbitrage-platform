package db

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// 新增：Uniswap Swap 记录表
type SwapLog struct {
	gorm.Model
	TxHash      string `gorm:"size:66;index"`
	Sender      string `gorm:"size:42"`
	ToAddr      string `gorm:"size:42"`
	Amount0In   string
	Amount1In   string
	Amount0Out  string
	Amount1Out  string
	Reserve0    string
	Reserve1    string
	Price       string
	BlockNumber uint64
}

func InitSwapDB() error {
	var err error
	DB, err = gorm.Open(sqlite.Open("chain.db?_journal=WAL"), &gorm.Config{})
	if err != nil {
		return err
	}

	// 自动迁移两个表
	return DB.AutoMigrate(&ChainEvent{}, &SwapLog{})
}
