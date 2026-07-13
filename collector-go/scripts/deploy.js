const { ethers } = require("hardhat");

async function main() {
  // 获取部署钱包
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // 查看余额
  const balance = await deployer.getBalance();
  console.log("Account balance:", ethers.utils.formatEther(balance));

  // -----------------------
  // 关键：Lock合约需要传入 unlockTime 参数
  // -----------------------
  const unlockTime = Math.floor(Date.now() / 1000) + 3600; // 1小时后解锁
  const Lock = await ethers.getContractFactory("Lock");
  
  // 这里必须传参数！
  const lock = await Lock.deploy(unlockTime);

  // 等待部署完成（ethers v5 正确写法）
  await lock.deployed();

  console.log(`Lock 合约已成功部署到地址: ${lock.address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });