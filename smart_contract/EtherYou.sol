pragma solidity >=0.4.22 <0.6.0;
pragma experimental ABIEncoderV2;

contract EtherYou {

    struct MessageRegister {
        uint timestamp;
        bytes32 blockHash;
        bytes messageBlock;
    }

    MessageRegister[] registry;

    constructor() public {
    }

    function sendMessage(bytes memory message) public {
        bytes32 blockHash = sha256(message);
        uint timestamp = now;
        MessageRegister memory mr = MessageRegister({timestamp: timestamp, blockHash: blockHash, messageBlock: message});
        registry.push(mr);
    }

    function getMessage(uint index) public view returns (uint, bytes memory){
        return (registry[index].timestamp, registry[index].messageBlock);
    }

    function getTimestamp(uint index) public view returns (uint){
        return registry[index].timestamp;
    }

    // Returns the index that has the target timestamp. If there is none, returns the index of the smallest timestamp that is greater than the target
    function getIndexOfTimestamp(uint target_timestamp) public view returns (uint) {
        uint L = 0;
        uint R = registry.length;
        uint m = 0;

        while (L < R){
            m = (L + R) / 2;
            if (registry[m].timestamp < target_timestamp){
                L = m + 1;
            }
            else{
                R = m;
            }
        }
        return L;
    }

    function getMessagesFromTimestamp(uint timestamp) public view returns (uint[] memory, bytes32[] memory, bytes[] memory){
        uint firstIndex = getIndexOfTimestamp(timestamp);
        uint numberOfMessages =  registry.length - firstIndex;
        uint[] memory timestamps = new uint[](numberOfMessages);
        bytes32[] memory hashes = new bytes32[](numberOfMessages);
        bytes[] memory messages = new bytes[](numberOfMessages);

        for(uint i = 0; i < messages.length; i++){
            timestamps[i] = registry[i+firstIndex].timestamp;
            hashes[i] = registry[i+firstIndex].blockHash;
            messages[i] = registry[i+firstIndex].messageBlock;
        }
        return (timestamps, hashes, messages);
    }
}
