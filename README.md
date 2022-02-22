# Practical Homework 2: Algorand Election dApp

In this homework you will build an election dApp (decentralized app), creating a smart contract on the Algorand network and a webapp frontend.

The smart contract will handle the logic and data for the election.

The webapp frontend will allow users to easily interact with the smart contract from their browser.

## Why do this homework

### Why Smart Contracts?

Smart contracts have seen a large uptick in use cases and are being adopted worldwide. Smart contracts utilize the blockchain's power to ensure **transparency**, **verifiability**, and **decentralization**.

- **Transparency** - The compiled code resides publicly on the blockchain. Any transaction interacting with the smart contract is also public.
- **Verifiability** - Users can verify that their interactions with the smart contract actually occurred and produced the exact results that were expected by looking at the public blockchain transactions
- **Decentralization** - There is no single point of failure since the blockchain network is decentralized.

#### Relevant articles

- [_What is a Smart Contract_](https://www.coinbase.com/learn/crypto-basics/what-is-a-smart-contract)
- [_Real-World Use Cases for Smart Contracts and dApps_](https://www.gemini.com/cryptopedia/smart-contract-examples-smart-contract-use-cases)
- [_Upgrading Blockchains Smart contract use cases in industry_](https://www2.deloitte.com/us/en/insights/focus/signals-for-strategists/using-blockchain-for-smart-contracts.html)

### Why Web frontends?

A large part of the reason for web frontends is accessibility. There are more than 4 billion people connected to the internet, with each one having an access to a browser. This makes a web frontend ideal to be accessible to as many people as possible.

## Background Concepts

### Smart Contract Overview

Algorand smart contracts are pieces of logic residing on the Algorand blockchain that once deployed, are remotely callable from any node. Once deployed, the on-chain instantiation of the contract is referred to as an Application and assigned an Application Id. These applications are triggered by a specific type of transaction called an Application Call transaction. These on-chain applications handle the primary decentralized logic of a decentralized application.

### Passing in arguments into smart contract arrays

A set of arrays can be passed with any application transaction that instructs the protocol how to load additional data used in the smart contract. These arrays include the applications, accounts, assets, and arguments array. In this assignment, you will only be dealing with the arguments and accounts array. The arguments array, limited to 16 arguments, allows you to pass standard arguments to the smart contract (in this case, handles passing in the voting election parameters defined in the global variables, the creator’s response to approve a user, or a user’s vote). The accounts array allows additional accounts to be passed to the contract for balance information and local storage.

### Storage and state manipulation

Storage can be either global or local. Global storage is data that is specifically stored on the blockchain for the contract globally. Global storage is limited to 64 key/value pairs. When a contract needs to store more data, for example to store data associated to each account that uses the smart contract (such as if the account is a registered voter), global storage cannot be used. Instead, local storage must be used. Local storage is also stored on the blockchain but contrary to global storage, there is one local storage per account that "opts in" in the contract.  You can manipulate states with following PyTeal operations:

- Reading and writing to application global state with `App.globalPut`, `App.globalGet`, `App.globalDel`.
- Reading and writing to account local state with `App.localPut`, `App.localGet`, `App.localDel`.
- Refer to this link for more specific syntax details: https://pyteal.readthedocs.io/en/stable/state.html


## Step 0 - Setup

### Step 0.0 - Complete Practical Homework

In [Practical Homework 1](https://github.com/PennCIS233/Practical-HW1) you install **Python** and **Pip**, setup your **PureStake account**, and install **PyCharm**.

If you have not setup any of those please refer to the [Practical HW 1](https://github.com/PennCIS233/Practical-HW1).

### Step 0.1 - Download Chrome and AlgoSigner

[Google Chrome](https://www.google.com/chrome) is a browser developed by Google and allows third-party extensions that a user downloads to interact with the webpages which that user visits.

[AlgoSigner](https://www.purestake.com/technology/algosigner/) is a Chrome browser extension created by PureStake which manages a user's Algorand keys, allowing that user to sign and send transactions (sending Algos or smart contract interactions) from their browser. Websites can prompt a transaction, and the user can see the transaction's details and choose whether or not to sign and send it from the AlgoSigner extension.

Once you have Google Chrome installed add the AlgoSigner extension at this [link](https://chrome.google.com/webstore/detail/algosigner/kmmolakhbgdlpkjkcjkebenjheonagdm?hl=en-US).

### Step 0.2 - Setup AlgoSigner Accounts

In Practical Homework 1 you created two Algorand accounts. Account A and Account B. Once you have Algorand installed on Chrome do the following.

- Import Account A and Account B into AlgoSigner **on the TestNet**
- Create 2 new accounts Account C and Account D using AlgoSigner **on the TestNet**
- Create as many other accounts as you would like

A walkthrough on how to do this can be seen here:  
[https://www.youtube.com/watch?v=tG-xzG8r770](https://www.youtube.com/watch?v=tG-xzG8r770)

**Remember to save and safeguard your password and mnemonics!**

### Step 0.3 - Fund AlgoSigner Accounts

In the same way as Practical Homework 1, in order to use your accounts they need to be funded. Use a [dispenser](https://bank.testnet.algorand.network/) to fund the accounts if they do not have Algos.

### Step 0.4 - Install PyTeal

Install the PyTeal library, `pyteal`, by typing this into your terminal:

```bash
python3 -m pip install pyteal
```

If you are using Windows, you may need to replace `python3` by `python` everywhere.

### Step 0.5 - Install Node.js and set up environment

First, check if you have Node installed by running `node -v; npm -v`. You should have a Node version of at least 12.

If you do not have Node.js, you can download it [here] (https://nodejs.org/en/download/).
If you are using MacOS, it is recommended to install Node.JS using [HomeBrew](https://brew.sh/) as follows:
```bash
brew install node
```

Next, download the files for this project. Open your terminal, and `cd` into the `frontend` directory. Once inside the directory, type `npm install`, which will download all the dependencies required for the project. Specifically, the dependencies specified in package.json will be downloaded into a node_modules/ directory.

To see if you have everything working, type `npm start`. You should see a basic webpage appear in your browser at localhost:3000. If you made it this far, then your setup has been successful!

## Step 1 - Create the smart contract

The smart contract is inside the `smart-contract` folder.

We recall that the smart contract will be written in Python using PyTeal.

### Design Overview:

In `election_smart_contract.py`, you will be creating a smart contract that conducts an election with multiple discrete choices. You will define each choice as a byte string and user accounts will be able to register and vote for any of the choices. There is a configurable election period defined by global variable, `ElectionEnd`, the [Algorand round](https://developer.algorand.org/docs/get-details/transactions/#current-round) (block number) when the election will end.

Voting Requirements: 

- An account must register in order to vote.
- The creator approves/rejects an account's ability to vote
- Accounts cannot vote more than once. 
- Accounts that close out of the application before the voting period has concluded, denoted by the global variable, `ElectionEnd`, will have their vote removed.

Smart contract process:

1. Creator deploys smart contract
2. User(s) opt-in to the contract
3. Creator approves/reject user's ability to vote
4. Approved user can cast vote once. Approved user who voted can remove their vote (potentially then revote) if they closeout or clear program
5. Repeat 2 to 4 for each user who opts-in before the election end
6. Election ends implicitly (from the current round being greater than the `ElectionEnd` round) and no further changes (opt-ins, votes, approvals/rejects) can be made to the election.
7. Clear state and close out can still occur, but if the election has ended then no change is made to the vote tallies.

Smart contracts are implemented using two programs:

- `ApprovalProgram`: Responsible for processing all application calls to the contract and implementing most of the logic of an application. Handles opting in, approving users to vote, and casting votes. Used to close out accounts and can control if a close out is allowed or not.
- `ClearStateProgram`: uses the clear call to remove the smart contract from the balance record of user accounts. This method of opting out cannot be stopped by the smart contract.

![alt text](https://github.com/PennCIS233/Practical-HW2/blob/main/smart-contract/Smart_Contract_Architecture.png)

### Global Variables

For standardization, we require everyone use the same global variable names in the approval program of the smart contract.


`ElectionEnd` (int)

- Round number for when the election will end
- Round number is how the algorand blockchain keeps track of time
- After this round number/time no more opting-in, voting, approvals, etc

`VoteOptions` (bytes)

- String consisting of all vote options concatenated together separated with commas
- Example: Abby, Barney, Cho, and Di are options then VoteOptions=”Abby,Barney,Cho,Di”

`NumVoteOptions` (int)

- Number of options to vote for
- We need this variable because Teal/Pyteal/Algorand doesn’t have arrays, so we store the vote options as a string (see above), so we need this variable to tell the smart contract how many voting options there are
- Example: Abby, Barney, Cho, and Di are options, so VoteOptions=”Abby,Barney,Cho,Di” and NumVoteOptions=4

`VotesFor0, VotesFor1, VotesFor2, etc` (int)

- Vote tally for option `i` where `i` is between `0` and `NumVoteOptions-1`
- Because PyTeal allows key-value variables, we can produce these variables in a for-loop on smart contract creation and access them when a user tries to vote using the index value of their vote option choice
- Example: VoteOptions=”Abby,Barney,Cho,Di”. VotesFor0 refers to vote tally for Abby. VotesFor1 refers to vote tally for Barney. VotesFor2 refers to vote tally for Cho. VotesFor3 refers to vote tally for Di

### Approval Program

#### `election_params.py`, `secrets.py`, `delete_app.py`

Copy the files `election_param.template.py` and `secrets.template.py` into `election_params.py` and `secrets.py`.

Input your token and the private mnemonics of the accounts you want to register for the voting election in `secrets.py`. One of these will be the Creator account. Input the election parameters in `election_params.py`, where you will declare local and global ints and bytes for the local and global state schema, and define the election period, and the voting options. 

`election_smart_contract.py` will import values from both these files as parameters for the election you will create and accounts who opt in and vote. You can create and deploy new smart contracts based on new parameters or accounts. Since each account can only create up to 10 apps unless apps are deleted, feel free to run delete_app.py to delete previously created apps if the limit is reached.

#### Step 1.1: Main Conditional 

The heart of the smart contract is a simple logical switch statement used to route evaluation to different sets of logic based on a Transaction's `OnComplete` value (defined in `create_app`). This logic allows the contract to choose which operation to run based on how the contract is called. For example, if `Txn.application_id()` is 0, then the on_creation sequence will run. If `Txn.on_completion()` is `OnComplete.OptIn`, the `on_register` sequence will run. If `Txn.application_args[0] == Bytes("vote")` then we want the `on_vote` sequence to be called. We've completed the first few cases for you.

**Note:** What you end up passing into `application_args[0]` is the identifier in the transaction for the action to perform. In this case, there are two main actions we want to check for: when an account wants to vote and when the creator wants to update the user’s voting status. Make sure the name of the identifier that is passed into `application_args[0]` is “vote” for the first action and “update_user_status” for the second action.

**TODO:** Implement the `program` conditional. 

#### Step 1.2: Creation

**TODO:** `on_create`: This sequence runs when the smart contract is created. It takes arguments from creation and puts them into the proper global variables.
- Store the values of election parameters passed from the application arguments of the election that was created.
  - `ElectionEnd` -the round number for the end of the election
  - `VoteOptions` - the different options to vote for,
  - `NumVoteOptions` - the number of options there are to vote for
- For all vote options, set initial vote tallies corresponding to all vote options to 0 where the keys are the vote options. (`VotesFor0`, `VotesFor1`, etc)

Although there are many ways to store the vote options, for the purposes of this project, we want you to store them as a string of options separated by commas e.g., "A,B,C,D". Note that index-wise, A=0, B=1, C=2, D=3. 



#### 1.3 Close-out

**TODO:** Implement `on_closeout`, which is called when user removes interaction with this smart contract from their account.
- Removes the user's vote from the correct vote tally **_if and only if_** the user closes out of program before the end of the election.
- Otherwise, does nothing

#### 1.4 Registration

**TODO:** Implement `on_register`, a function that is called when sender/user opts-in to the smart contract. 
- Ensure that the user is registering before the election end
- If so, in the user's account's local storage set the `can_vote` variable to `"maybe"`

#### 1.5 Update user logic

**TODO:** Implement `on_update_user_status`, which is called when creator wants to approve/disapprove of a user who opted-in the election.
- Fetch the creator's decision to approve or reject a user acccount and update user's voting status accordingly.
- [Assert](https://pyteal.readthedocs.io/en/stable/control_structures.html#checking-conditions-assert) the following: only the creator of the smart contract can approve or disapprove users and users can only be approved before the election ends and the creator cannot update a given user's status more than once.
- Think about how the given user's address and creator's decision are stored
- You should set the user's `can_vote` local state variable to what the creator has decided: `"yes"` or `"no"`

The `on_update_user_status` sequence expects the following values in arguments 1 and 2 of the `Txn.application_args` array:
- `address_to_approve` (bytes): 32-byte address that creator wants to approve/disapprove
- `is_user_approved` (bytes): “yes” if creator wants address to be able to vote, “no” if the creator wants address to not be able to vote

#### 1.6 User Voting Logic:

**TODO:** Implement `on_vote`, a function that is called when the txn sender/user votes. The logic in this sequence properly casts a user's vote and updates the local and global states accordingly.
- [Assert](https://pyteal.readthedocs.io/en/stable/control_structures.html#checking-conditions-assert) that the election isn't over and that user is allowed to vote using `get_sender_can_vote`.
- Check using `get_vote_of_sender` to check if the user has already voted. If so, return a 0. Otherwise, get the choice that the user wants to vote for from the application arguments.
- [Assert](https://pyteal.readthedocs.io/en/stable/control_structures.html#checking-conditions-assert) that the vote choice is within index bounds of the vote options.
- Update the vote tally for the user's choice under the corresponding global variables.
- Record the user's vote index in their account's local storage under the key `voted`

`on_vote` variables:

- choice (int): Index for option the sender/user wants to vote for



### Clear State Program

**TODO:** Implement the `clear_state_program()` function, which handles the logic of when an account clears its participation in a smart contract. 
- Just like the `close_out` sequence, if the user clears state of program before the end of voting period then it removes their vote from the correct vote tally. Otherwise, it doesn't do anything.


## Step 2 - Implement the smart contract deploy script

In the deploy script, you will deploy the voting contract using an ApplicationCall transaction in `create_app` and complete the `main()` function.

**TODO:** Implement `create_app`. The creator will deploy the app using this method. This method has 7 parameters:
- `sender`: address, representing the creator of the app
- `sp`: suggested parameters obtained from the network
- `on_complete`: enum value, representing NoOp. Describes the action to be taken following the execution of the approval program or clear state program. 
- `approval_program`: compiled program
- `clear program`: compiled program
- `local_schema`: maximum local storage allocation, immutable
- `global_schema`: maximum global storage allocation, immutable



**TODO:** Implement `deploy_create_app`. First, compile the approval and clear state programs to TEAL assembly, then to binary. Create the application and the application arguments which should include a list of election parameters you defined previously as global variables: `election_end`, `num_vote_options`, `vote_options`.

**TODO:** Implement the `main()` function where you initialize the algod client and define absolute election end time fom the status of the last round. Deploy the application and print the global state.


### Test smart contract using `simple_tests.py`

Test your smart contract functions by running the testing script simple_tests.py. Feel free to add your own tests as the ones we have provided are not comprehensive. We only test that basic functionalities are working, namely the creation and initial variable setup, two users opting in, the creator correctly approving two users, approved users being able to vote, and closing out the app. 


## Step 3 - Frontend Logic: `AlgoHandler.js`

If our frontend wants to display relevant information to our users it will need a way to retrieve data from the Algorand blockchain. Similarly, if our frontend wants to allow users to interact with our election smart contract our frontend will need to be able to send transactions to the Algorand blockchain. We will make use of the PureStake Algod client and Indexer client to retrieve information about the current state of our smart contract. We will use the AlgoSDK and AlgoSigner to create, sign, and send transactions to be added to the Algorand TestNet.

#### How

`frontend/src/utils/AlgoHandler.js` is meant to contain all functionality related to retrieving information about the smart contract and sending transactions to the Algorand TestNet.

### Step 3.0 - Getting Familiar with the Tools

#### JavaScript

We do not assume that you have extensive knowledge about JavaScript. JavaScript is a very newcomer-friendly language that aligns nicely with other languages' syntax and paradigms. You will need to know variables, functions, loops, conditionals, and async/await in JavaScript. Here are some resources to get you started:

- [Learn javascript in Y Minutes](https://learnxinyminutes.com/docs/javascript/ "Learn javascript in Y Minutes") - basic JavaScript information
- [The await keyword](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await#the_await_keyword "The await keyword") - Essentially all you need to know about async/await for this homework
- Google - We highly encourage you to search for documentation, tutorials, and other resources if you would like to know more about any functionality or design patterns in JavaScript (how to iterate through an array, ternary operations, etc)

#### AlgoSDK

In Practical Homework 1 and parts of this homework you have used the Python version of the AlgoSDK. The frontend will make use of the JavaScript version of the AlgoSDK. Both versions are very similar in functionality and even close in syntax.

In general, smart contracts are implemented using `ApplicationCall` transactions in the AlgoSDK. These transaction types are as follows:
- `NoOp` - Generic application calls to execute the `ApprovalProgram`.
- `OptIn` - Accounts use this transaction to begin participating in a smart contract. Participation enables local storage usage.
- `DeleteApplication` - Transaction to delete the application.
- `UpdateApplication` - Transaction to update TEAL Programs for a contract.
- `CloseOut` - Accounts use this transaction to close out their participation in the contract. This call can fail based on the TEAL logic, preventing the account from removing the contract from its balance record.
- `ClearState` - Similar to `CloseOut`, but the transaction will always clear a contract from the account’s balance record whether the program succeeds or fails.

You will be using the types of transaction application calls mentioned above to implement the `optInAccount`, `updateUserStatus`, `vote`, `closeOut`, and `clearState` functions in our `AlgoHandler.js` file.

Take a look at the documentation here to understand how the Javscript AlgoSDK interacts with smart contracts and the specific syntax to use:

- [https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/)
- https://algorand.github.io/js-algorand-sdk/

#### AlgoSigner

You downloaded the AlgoSigner extension in step 0. Now any website visited will have AlgoSigner code injected into the website that can be used by the website. This code can be accessed through the variable `window.AlgoSigner`.

Here is some useful documentation:

- https://github.com/PureStake/algosigner/blob/develop/docs/dApp-integration.md#working-with-transactions
- https://purestake.github.io/algosigner-dapp-example/

#### Purestake Indexer API

Purestake has an API setup for querying historical data from the Algorand blockchain. You will use this API to retrieve data on who has opted-in to your election.

Take a look at this example to see how it uses the Indexer to read the local state of all accounts which opted-in to the application: https://developer.algorand.org/solutions/example-digital-exchange-smart-contract-application/

In `frontend/src/utils/` create a new file `frontend/src/utils/secrets.js` with the same format as `frontend/src/utils/secrets.template.js` using your PureStake API key.

#### AlgoHandler.js `frontend/src/utils/AlgoHandler.js`

This file exports a singular instance of the class it contains which is meant to encapsulate data retrieval and transaction-sending from and to the Algorand blockchain.

We provide you a skeleton outline with all the necessary functions needed for you to fill out. You will be graded on producing the correct outputs for these functions (for those that have a specified return) and for sending the correct properly-formatted transactions (for those that require sending a transaction) .

### Step 3.1 - AlgoHandler constructor

In `frontend/src/utils/AlgoHandler.js` fill out the `TODO` sections. Remember, don't change the variable names. You can define additional variables if needed.

- Set the `this.algodClient` variable
- Set the `this.indexerClient` variable

### Step 3.2 - Retrieving Data

In `frontend/src/utils/AlgoHandler.js` fill out the following 4 functions with the commented functionality. Remember, don't change the function names. Feel free to add helper functions if you want. Remember to use JavaScript's `await` keyword appropriately when using `this.algodClient`, `this.algodIndexer`, and `window.AlgoSigner`

#### Relevant Documentation

- https://developer.algorand.org/solutions/example-digital-exchange-smart-contract-application/
- https://github.com/PureStake/algosigner/blob/develop/docs/dApp-integration.md#algosignerconnect
- https://developer.algorand.org/docs/archive/build-apps/connect/

1. `getAlgoSignerAccounts()`
    - **TODO:** Connect to AlgoSigner
    - **TODO:** Retrieve all addresses in array format and return them
2. `getLatestRound()`
    - **TODO:** Retrieve the Algod client status
    - **TODO:** Return the `"last-round"` value of the retrieved status
3. `getElectionState(appID)`
    - **TODO:** Use `this.algodClient` to retrieve the app details
    - The rest is filled out for you :)
    - Look over the logic and look at the returned value
4. `getAllLocalStates(appID)`
    - **TODO:** Use `this.indexerClient` to find all accounts who are associated with the given app
    - **TODO:** Take the data and format it into a neat JavaScript object (nearly equivalent to a Python dictionary) as specified
      - Example:
      ```javascript
        allLocalStates = {
          // example acccount 1
          'jsdalkfjsd...': {
            'can_vote': 'yes',
            'voted': 2
          },
          // example account 2
          'fdsfdsaf...': {
            'can_vote': 'no'
          },
          // example account 3
          'asdffdsaf...': {
            'can_vote': 'maybe'
          }
        }
      ```
      - **Note:** Only include values that are included in the original object. If a user does not have a value for `voted` then don't include the `voted` variable

### Step 3.3 - Sending Transactions

In `frontend/src/utils/AlgoHandler.js` fill out the following 6 functions with the commented functionality. Remember, don't change the function names. Feel free to add helper functions if you want. Remember to use JavaScript's `await` appropriately when using `this.algodClient`, `this.algodIndexer`, and `window.AlgoSigner`

#### Relevant Documentation

- https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/#application-methods
- https://github.com/PureStake/algosigner/blob/develop/docs/dApp-integration.md#algosignersigntxntxnobjects
- https://algorand.github.io/js-algorand-sdk/

1.  `signAndSend(txn)`
    - **TODO:** Convert the transaction to Base64 with AlgoSigner's method
    - **TODO:** Sign the base64 transaction with AlgoSigner
    - **TODO:** Send the message with AlgoSigner
2.  `optInAccount(address, appID)`
    - **TODO:** Get the suggested params from `this.algodClient`
    - **TODO:** Create the opt-in transaction
    - **TODO:** Sign and send the transaction with our `this.signAndSend` function
3.  `updateUserStatus(creatorAddress, userAddress, yesOrNo, appID)`
    - **TODO:** Get the suggested params from `this.algodClient`
    - **TODO:** Set up the transaction app arguments (remember the first argument should be the smart contract method identifier, in this case that's `"update_user_status"` )
    - **TODO:** Create the transaction
      - Include both the creator's address and user's address in the optional address array when creating the transaction (different from app args)
    - **TODO:** Sign and send the transaction with our `this.signAndSend` function
4.  `vote(address, optionIndex, appID)`
    - **TODO:** Create app parameters (remember the first argument should be the smart contract method identifier, in this case that's `"vote"` )
    - **TODO**, create transaction, sign and send
5.  `closeOut(address, appID)`
    - **TODO:** Create transaction, sign and send, similar to above
6.  `clearState(address, appID)`
    - **TODO:** Create transaction, sign and send, similar to above

## Bonus - A brief tour of our React application

In this project, we have pre-built the React application for you to connect to, but we'll briefly touch over the file structure of our project.

First, React is a JavaScript library for building user interfaces. It utilizes a **component-based** structure that encapsulates its own state. Within each component, we specify state (which are variables such as the election ID, or user accounts) and then return a snippet of code that tells React how to render the component. For more information about React itself, you can find the documentation [here] (https://reactjs.org/docs/hello-world.html). We also utilize the `react-bootstrap` library, which has out-of-the-box components to create a nicer UI. Read more about it [here] (https://react-bootstrap.github.io/components/alerts).

Pages:

- **ConnectPage.js**: The ConnectPage prompts the user to connect to the AlgoSigner browser extension, and once the user is connected, allows the user to input the election id.
- **ElectionPage.js**: The ElectionPage holds the majority of the functionality: it lets you see all participants in the election, view information about the election, and allows the user to participate in the election.

Components:

- **NavBar.js**: The NavBar component allows the participant to choose your current account, so you can participate in the election from that account.
- **ElectionInfoCard.js**: The ElectionInfoCard component displays the election creator, the last round to participate in the election, the number of votes, the vote options, and a pie chart displaying the vote distribution.
- **ParticipantsCard.js**: The ParticipantsCard component has three tabs: accepted, rejected, and pending. Each of these categories has a list of participants. The list of accepted users also contains the vote that they chose if they have made one. The list of pending users will also contain Accept/Reject buttons if the current account is a creator account.
- **VoterCard.js**: The VoterCard component displays a card that will
- **AlgoHandler.js**: The AlgoHandler component contains many helper functions that you will be implementing. You will have to implement functions to interact with the election, such as voting and opting-in, as well as functions to retrieve information about the state of the election.

We highly recommend taking a look at the files themselves, so that you have a good sense of how the frontend works!

You can try running the app in your Chrome browser by running `npm start` in the `frontend/voting-app` folder. 
