// pragma solidity >=0.7.0 <0.9.0;

// contract UserCredentials {

//     struct User {
//         string username;
//         string email;
//         string password;
//     }

//     User[] public users;

//     function addUser(string memory username, string memory email, string memory password) public {
//         users.push(User(username, email, password));
//     }

// function getUser(string memory userEmail) public view returns (string memory, string memory, string memory) {
//     for (uint i = 0; i < users.length; i++) {
//         if (keccak256(abi.encodePacked(users[i].email)) == keccak256(abi.encodePacked(userEmail))) {   
//             return (users[i].username, users[i].password, users[i].email);
//         }
//     }
//     revert("User does not exist. Email: ");
// }


// }



// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract UserCredentials {

    struct User {
        string username;
        string email;
        string password;
    }

    User[] public users;

    function addUser(string memory username, string memory email, string memory password) public {
        users.push(User(username, email, password));
    }
function getUser(string memory userEmail) public view returns (string memory, string memory, string memory) {
    bytes32 userEmailHash = keccak256(abi.encodePacked(userEmail));
    for (uint i = 0; i < users.length; i++) {
        if (keccak256(abi.encodePacked(users[i].email)) == userEmailHash) {   
            return (users[i].username, users[i].password, users[i].email);
        }
    }
    revert("User does not exist. Email: ");
}

}
