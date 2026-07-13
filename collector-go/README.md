# Web3 链上事件监控系统（Go + Ethereum）

## 项目介绍
基于 Golang 开发的企业级链上事件监听服务，支持：
- 以太坊 Sepolia 公链事件实时监控
- ABI 标准事件解析
- 数据持久化（SQLite）
- 防重复入库、区块轮询、自动重连
- HTTP API 接口提供数据查询

## 技术栈
- Go
- Ethereum Sepolia
- Infura WSS
- SQLite(GORM)
- Gin API

## 核心功能
1. 监听合约 Withdrawal 事件
2. 链上数据解析与结构化存储
3. 7x24 稳定后台运行
4. API 接口支持外部系统对接

## 部署信息
- 合约地址：0x78B691Fac809bF8Df3Fd6E1B70c11b15Ca9934AB
- 网络：Sepolia Testnet