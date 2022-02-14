const algosdk = require("algosdk");

// This will handle all algosdk, indexer, and AlgoSigner code
class AlgoHandler {
  constructor() {
    // waits a little while then checks to see if the AlgoSigner extension is installed
    setTimeout(200, () => {
      if (typeof window.AlgoSigner == "undefined") {
        console.log("Please install the AlgoSigner extension");
        alert("Please install the AlgoSigner extension");
        return;
      }
    });
    console.log("New AlgoHandler");

    // Setup the algod client using your PureStake token, and Purestake algod server url
    // TODO -----------------------------------------------------------------------------
    this.algodClient = null;

    // Setup the indexer client using your PureStake token, and PureStake indexer server url
    // TODO -----------------------------------------------------------------------------
    this.indexerClient = null;
  }

  // getAlgoSignerAccounts
  // Description:
  //  Attempts to connect to the accounts present in the browser's AlgoSigner addon
  // Returns:
  //  accounts (string[]) - string array of all account addresses
  async getAlgoSignerAccounts() {
    // This variable will be returned after populated
    var accounts = [];

    // Attempt to connect to AlgoSigner, note you will have to use the 'await' keyword
    // If this fails or an error occurs, return an empty array
    // TODO -----------------------------------------------------------------------------


    // Retrieve all the AlgoSigner accounts on the TestNet
    // Note they may be in this format: [{address: 'address1'}, {address: 'address2'}, etc]
    // TODO -----------------------------------------------------------------------------


    // Return the accounts in array format: ['address1', 'address2', 'address3', etc]
    return accounts;
  }

  // isCreator
  // Description:
  //  Checks and returns boolean on whether the given user (address) is the creator of the given app (appID)
  // Parameters:
  //  appID (number) - ID of the app
  //  address (string) - address of the specified user's account, the address of the alleged creator
  // Returns:
  //  returns (bool) - whether the given address is the creator of the election at electionAddress
  async isCreator(appID, address) {
    // There are two potential ways to accomplish this task
    // The first is to check the created apps of the user and see if the appID is included
    // The second is to check the global state of the smart contract and compare the decoded 'Creator' value
    // TODO -----------------------------------------------------------------------------
  }

  // decodes bytes to strings for values from the smart contract app
  decode(encoded) {
    return Buffer.from(encoded, "base64").toString();
  }

  // getElectionState
  // Description:
  //  Retrieves and returns the current global variable values in the given app (appID)
  // Parameters:
  //  appID (number) - id (aka index) of the Algorand smart contract app
  // Returns:
  //  returns (object) - Javascript object of election variables to their values
  //  example:
  //   {
  //     'Creator': 'fjlasjfskfa...',
  //     'VotesFor0': 0,
  //     'VotesFor1': 0,
  //     'VoteOptions': 'A,B,C,D',
  //     ...
  //   }
  async getElectionState(appID) {
    // newState will be returned once it's filled with data
    let newState = {};

    // Use the algodClient to get the the app details
    // TODO -----------------------------------------------------------------------------

    // The data might have a complex structure, feel free to console.log it to see the structure

    // Go through the data and add the global state variables and values to our newState object (dictionary)
    console.log("Application's global state:");
    for (let x of app["params"]["global-state"]) {
      console.log(x);

      // decode the object key
      let key = this.decode(x["key"]);

      // Bytes values need to be decoded
      // Addresses stored as bytes  need a special decoding process which we have done for you :)
      let bytesVal =
        key == "Creator"
          ? algosdk.encodeAddress(Buffer.from(x["value"]["bytes"], "base64"))
          : this.decode(x["value"]["bytes"]);
      
      // uint types don't need to be decoded
      let uintVal = x["value"]["uint"];

      // type is 1 if the variable is the bytes value, 2 if the variable is actually the uint value
      let valType = x["value"]["type"];

      // set the value for the key in our newState object to the correct value
      newState[key] = valType == 1 ? bytesVal : uintVal;
    }

    // return the newState
    return newState;
  }

  // getAllLocalStates
  // Description:
  //  Takes a given appID and finds all accounts that have opted-in to it, then returns all users' decoded local states
  // Parameters:
  //  appID (number) - id (aka index) of the Algorand smart contract app
  // Return:
  //  returns (object) - Javascript object (dictionary) of addresses mapped to their states
  //  example: 
  //   {
  //     'jsdalkfjsd...': {
  //       'can_vote': 'yes', 
  //       'voted': 2
  //     }, 
  //     'fdsfdsaf...': {
  //       'can_vote': 'no'
  //     },
  //     'asdffdsaf...': {
  //       'can_vote': 'maybe'
  //     },
  //   }
  async getAllLocalStates(appID) {
    // allLocalStates will be returned once it's filled with data
    let allLocalStates = {};

    // Use this.indexerClient to find all the accounts who have appID associated with their account
    // TODO -----------------------------------------------------------------------------

    // The resultant JavaScript object (dictionary) may have a complex structure
    // Try to console.log it out to see the structure

    // Go through the data and fill allLocalStates to contain all the users' local states
    // Note that the *keys* of smart contract local state variables will need to be decoded using 
    //   Buffer.from(value, "base64").toString() or, equivalently, our helper this.decode(value) function
    // The actual values will also need to be decoded if they are bytes
    // If they are uints they do not need decoding
    // TODO -----------------------------------------------------------------------------

    // Return your JavaScript object
    return allLocalStates;
  }

  // signAndSend
  // Description:
  //  Signs the given transaction using AlgoSigner then sends it out to be added to the blockchain
  // Parameters: 
  //  txn (algosdk transaction) - transaction that needs to be signed
  async signAndSend(txn) {
    // transactions will need to be encoded to Base64. AlgoSigner has a builtin method for this
    // TODO -----------------------------------------------------------------------------


    // sign the transaction with AlgoSigner
    // TODO -----------------------------------------------------------------------------


    // send the message with AlgoSigner
    // TODO -----------------------------------------------------------------------------
  }

  // optInAccount
  // Description:
  //  Sends a transaction that opts in the given user (address) to the given app (appID)
  // Parameters:
  //  address (string) - address of the user who wants to opt into the election
  //  appID (number) - app id (aka index) of the smart contract app
  async optInAccount(address, appID) {
    // get the suggested params for the transaction
    // TODO -----------------------------------------------------------------------------

    // create the transaction to opt in
    // TODO -----------------------------------------------------------------------------

    // sign and send the transaction with our helper this.signAndSend function
    // TODO -----------------------------------------------------------------------------

  }

  // updateUserStatus
  // Description:
  //  sends a transaction from the creator (creatorAddress) to the given app (appID) to approve/reject the given user (userAddress)
  // Parameters:
  //  creatorAddress (string) - address of the creator who is allowed to approve for the transaction
  //  userAddress (string) - address of the user who is being approved/rejected
  //  yesOrNo (string) - "yes" or "no" depending on if the creator wants the user to be allowed to vote or not
  //  appID (number) - app id (aka index) of the smart contract app
  async updateUserStatus(creatorAddress, userAddress, yesOrNo, appID) {
    // get the suggested params for the transaction
    // TODO -----------------------------------------------------------------------------

    // setup the application argument array, note that application arguments need to be encoded
    // strings need to be encoded into Uint8Array
    // addresses, *only* when passed as *arguments*, need to be decoded with algosdk inbuilt decodeAddress function
    // and then use the public key value
    // TODO -----------------------------------------------------------------------------

    // create the transaction with proper app argument array
    // For this application transaction make sure to include the optional array of accounts including both the 
    // creator's account and also the user's account 
    // (both in regular string format, algosdk automatically converts these)
    // TODO -----------------------------------------------------------------------------

    // sign and send the transaction with our helper this.signAndSend function
    // TODO -----------------------------------------------------------------------------
  }

  // vote
  // Description:
  //  Sends a transaction from the given user (address) to vote for the given option (optionIndex) in the given election app (appID)
  // Parameters:
  //  address (string) - address of the user trying to vote
  //  optionIndex (number) - index (starting at 0) corresponding to the user's vote, ie in 'A,B,C' C would be index 2
  //  appID (number) - app id (aka index) of the smart contract app
  async vote(address, optionIndex, appID) {
    // TODO -----------------------------------------------------------------------------
  }

  // closeOut
  // Description:
  //  sends a transaction from given user (address) to closeout of the given app (appID)
  // Parameters:
  //  address (string) - address of the user trying to closeout of app
  //  appID (number) - app id (aka index) of the smart contract app
  async closeOut(address, appID) {
    // TODO -----------------------------------------------------------------------------
  }

  // clearState
  // Description:
  //  sends a transaction from the given user (address) to the given app (appID) to clear state of the app
  // Parameters:
  //  address (string) - address of the user trying to clear state of the app
  //  appID (number) - app id (aka index) of the smart contract app
  async clearState(address, appID) {
    // TODO -----------------------------------------------------------------------------
  }
}

// create and export a singular AlgoHandler instance
var mainAlgoHandler = new AlgoHandler();

export default mainAlgoHandler;
