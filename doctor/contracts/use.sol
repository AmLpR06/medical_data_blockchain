// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract UserCredentials {

    struct user {
        address id;
        string email;
        string username;
        string password;
    }

    // User[] public users;
    mapping(address=>user) users;

    function addUser(string memory username, string memory email, string memory password , address add) public returns(string memory) {
        if(users[add].id==add){
            return("Already Registered");
        }
        users[add].username=username;
        users[add].email=email;
        users[add].password=password;
        users[add].id=add;
        return("Succesfully Registered");
    }
 function getUser(string memory userEmail, address add) public view returns (string memory, string memory, string memory) {
        require(users[add].id == add, "User does not exist. Address not registered.");
     if (keccak256(abi.encodePacked(users[add].email)) == keccak256(abi.encodePacked(userEmail))) {
            return (users[add].username, users[add].password, users[add].email);
        }
        
        revert("User does not exist. Email does not match.");
       
    }


}
