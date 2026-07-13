pragma solidity ^0.8.28;

contract MySwapMonitor {
    // 你 Go 要监听的事件，indexed 方便过滤
    event SwapTriggered(
        address indexed sender,
        uint256 indexed ethAmount,
        uint256 minReturn,
        address indexed to
    );

    // 调用就发事件，永远不会失败
    function triggerEvent(uint256 minReturn) external payable {
        emit SwapTriggered(
            msg.sender,
            msg.value,
            minReturn,
            msg.sender
        );
    }
}