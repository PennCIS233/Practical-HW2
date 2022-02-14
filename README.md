# Practical Homework 1: Algorand Election dApp

In this homework you will build an election dApp (decentralized app), creating a smart contract on the Algorand network and a webapp frontend.

The smart contract will handle the logic and data for the election.

The webapp frontend will allow users to easily interact with the smart contract from their browser.

## Why do this homework

### Why Smart Contracts?

Smart contracts have seen a large uptick in use cases and are being adopted worldwide as a method of decentralized. Smart contracts utilize the blockchain's power to ensure **transparency**, **verifiability**, and **decentralization**.

- **Transparency** - The compiled code resides publicly on the blockchain. Any transaction interacting with the smart contract is also public.
- **Verifiability** - User's can verify that their interactions with the smart contract actually occurred and produced the exact results that were wanted by looking at the public blockchain transactions
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

A set of arrays can be passed with any application transaction that instructs the protocol how to load additional data used in the smart contract. These arrays include the applications, accounts, assets, and arguments array. In this assignment, you will only be dealing with the arguments and accounts array. The arguments array, limited to 16 arguments, allows you to pass standard arguments to the arguments (in this case, handles passing in the voting election parameters defined in the global variables, the creator’s response to approve a user, or a user’s vote). The accounts array allows additional accounts to be passed to the contract for balance information and local storage.

### Storage and state manipulation

Storage can be either global or local. Local storage refers to storing values in an accounts balance record if that account participates in the contract. Global storage is data that is specifically stored on the blockchain for the contract globally. You can manipulate states with following PyTeal operations:

- Reading and writing to application global state with App.globalPut, App.globalGet, App.globalDel.
- Reading and writing to account local state with App.localPut, App.localGet, App.localDel.
- Refer to this link for more specific syntax details: https://pyteal.readthedocs.io/en/stable/state.html

## Overview

### Tools

## Step 0 - Setup

### Step 0.0 - Complete Practical Homework

1 In [Practical Homework 1](https://github.com/PennCIS233/Practical-HW1) you install **Python** and **Pip**, setup your **PureStake account**, and install **PyCharm**.

If you have not setup any of those please refer to the [Practical HW 1](https://github.com/PennCIS233/Practical-HW1).

### Step 0.1 - Download Chrome and AlgoSigner

[Google Chrome](https://www.google.com/chrome) is a browser developed by Google and allows third-party extensions that a user downloads to interact with the webpages which that user visits.

[AlgoSigner](https://www.purestake.com/technology/algosigner/) is a Chrome browser extension created by PureStake which manages a user's Algorand keys, allowing that user to sign and send transactions (sending Algos or smart contract interactions) from their browser. Websites can prompt a transaction, and the user can see the transaction's details and choose whether or not to sign and send it from the AlgoSigner extension.

Once you have Google Chrome installed add the AlgoSigner extension at this [link](https://chrome.google.com/webstore/detail/algosigner/kmmolakhbgdlpkjkcjkebenjheonagdm?hl=en-US).

### Step 0.2 - Setup AlgoSigner Accounts

In practical homework 1 you created two Algorand accounts. Account A and Account B. Once you have Algorand installed on Chrome do the following.

- Import Account A and Account B into AlgoSigner **on the TestNet**
  - Save the addresses in form.md
- Create 2 new accounts Account C and Account D using AlgoSigner **on the TestNet**
  - Save the addresses in form.md

A walkthrough on how to do both of these can be seen here:  
[https://www.youtube.com/watch?v=tG-xzG8r770](https://www.youtube.com/watch?v=tG-xzG8r770)

**Remember to save and safeguard your password and mnemonics!**

### Step 0.3 - Fund AlgoSigner Accounts

In the same way as practical homework 1, in order to use your accounts you need to fund them. Use a [dispenser](https://bank.testnet.algorand.network/) to fund the accounts.

### Step 0.4 - Install PyTeal

Install the PyTeal library, `pyteal`, by typing this into your terminal:

```bash
pip3 install pyteal
```

### Step 0.5 - Install Node.js and set up environment

First, check if you have Node installed by running `node -v; npm -v`. You should have a Node version of at least x.x.x.

If you do not have Node.js, you can download it [here] (https://nodejs.org/en/download/).

Next, download the files for this project. Open your terminal, and `cd` into the TODO directory. Once inside the directory, type `npm install`, which will download all the dependencies required for the project. Specifically, the dependencies specified in package.json will be downloaded into a node_modules/ directory.

To see i fyou have everything working, type `npm start`. You should see a basic webpage appear in your browser at localhost:3000. If you made it this far, then your setup has been successful!

## Step 1 - Create the smart contract

### Design Overview:

In `election_smart_contract.py`, you will be creating a smart contract that conducts an election with multiple discrete choices. You will define each choice as a byte string and user accounts will be able to register and vote for any of the choices. There is a configurable election period defined by global variable, `ElectionEnd` which is relative to the current time

- An account must register in order to vote
- Accounts cannot vote more than once. Accounts that close out of the application before the voting period has concluded, denoted by the global variable, ElectionEnd
- The creator of the election has to approve every account that opts in

Here's simplified overview of the election smart contract:

1.  Creator deploys smart contract
2.  User(s) opt-in to the contract
3.  Creator approves/reject user's ability to vote
4.  Approved user can cast vote once
    4b. Approved user who voted can remove their vote (potentially then revote) if they closeout or clear program
5.  Repeat 2 to 4 for each user who opts-in before the election end
6.  Election ends and no further changes (opt-ins, votes, approvals/rejects) can be made to the election

Smart contracts are implemented using two programs:

- `ApprovalProgram`: Responsible for processing all application calls to the contract and implementing most of the logic of an application. Handles opting in, approving users to vote, and casting votes. Used to close out accounts and can control if a close out is allowed or not.
- `ClearStateProgram`: uses the clear call to remove the smart contract from the balance record of user accounts. This method of opting out cannot be stopped by the smart contract.

### Global Variables

For standardization, we require everyone use the same global variable names in the approval program of the smart contract.

`Creator` (bytes)

- 32-byte address of the deployer of the smart contract

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

- Vote tally for option i where i is between 0 and NumVoteOptions
- Because PyTeal allows key-value variables, we can produce these variables in a for-loop on smart contract creation and access them when a user tries to vote using the index value of their vote option choice
- Example: VoteOptions=”Abby,Barney,Cho,Di”. VotesFor0 refers to vote tally for Abby. VotesFor1 refers to vote tally for Barney. VotesFor2 refers to vote tally for Cho. VotesFor3 refers to vote tally for Di

### Approval Program

#### Main Conditional

The heart of the smart contract is a simple logical switch statement used to route evaluation to different set of logic based on a Transaction's `OnComplete` value (defined in `create_app`). This logic allows the contract to choose which operation to run based on how the contract is called. For example, if Txn.application_id() is 0, then the on_creation sequence will run. If `Txn.on_completion()` is `OnComplete.OptIn`, the `on_register` sequence will run. We've completed the first few cases for you.

#### Creation

Implement `on_create`: This sequence runs when the smart contract is created. It takes arguments from creation and puts them into the proper global variables.

Step 1: Store the values of election parameters passed from the application arguments of the election that was created.

- the creator as whoever deployed the smart contract
- the round number for the end of the election
- the different options to vote for,
- the number of options there are to vote for

Although there are many ways to store the vote options, for the purposes of this project, we want you to store them as a string of options separated by commas e.g., "A,B,C,D". Note that index-wise, A=0, B=1, C=2, D=3

Step 2: For all vote options, set initial vote tallies corresponding to all vote options to 0 where the keys are the vote options.

#### Close-out

Implement `on_closeout`, which is called when user removes interaction with this smart contract from their account.

Step 1: Removes the user's vote from the correct vote tally if the user closes out of program before the end of the election.

Step 2: Check that the voter is still in the election period and has actually voted. If so, update vote tally by subtracting one vote for whom the user voted for.

#### Registration

Implement `on_register`, a function that is called when sender/user opts-in to the smart contract
Check users are registering before the end of the election period and set user's voting status to "maybe."

#### Update user logic

Implement `on_update_user_status`, which is called when creator wants to approve/disapprove of a user who opted-in the election.
`on_update_user_status` variables:

- address_to_approve (bytes): 32-byte address that creator wants to approve/disapprove
- is_user_approved (bytes): “yes” if creator wants address to be able to vote, “no” if the creator wants address to not be able to vote

Step 1: Fetch the creator's decision to approve or reject a user acccount and update user's voting status accordingly.

Step 2: Only the creator can approve or disapprove users and users can only be approved before the election ends.

Step 3: Think about how the given user's address and creator's decision are stored

#### User Voting Logic:

Implement `on_vote`, a function that is called when the txn sender/user votes. The logic in this sequence properly casts a user's vote and updates the local and global states accordingly.

`on_vote` variables:

- choice (int): Index for option the sender/user wants to vote for

STEP 1: Check that the election isn't over and that user is allowed to vote using get_sender_can_vote.

STEP 2: Check using `get_vote_of_sender` to check if the user has already voted. If so, return a 0. Otherwise, get the choice that the user wants to vote for from the application arguments.

STEP 3: Update the vote tally for the user's choice under the corresponding global variables.

STEP 4: Record the user has successfully voted by writing the choice they voted for to the user's "voted" key to reflect their choice. Make sure that the vote choice is within index bounds of the vote options.

### Clear State Program

Implement the `clear_state_program()` function, which handles the logic of when an account clears its participation in a smart contract. Just like the `close_out` sequence, ensure the user clears state of program before the end of voting period and remove their vote from the correct vote tally.

## Step 2 - Implement the smart contract deploy script

In the deploy script, you will implement functions that are used to interact with the smart contract and deploy the voting contract in the `main()` function.

Smart contracts are implemented using `ApplicationCall` transactions. These transaction types are as follows:

- `NoOp` - Generic application calls to execute the `ApprovalProgram`.
- `OptIn` - Accounts use this transaction to begin participating in a smart contract. Participation enables local storage usage.
- `DeleteApplication` - Transaction to delete the application.
- `UpdateApplication` - Transaction to update TEAL Programs for a contract.
- `CloseOut` - Accounts use this transaction to close out their participation in the contract. This call can fail based on the TEAL logic, preventing the account from removing the contract from its balance record.
- `ClearState` - Similar to `CloseOut`, but the transaction will always clear a contract from the account’s balance record whether the program succeeds or fails.

Step 1: Implement the `create_app`, `opt_in_app`, `call_app_approve_voter`, `call_app`, `delete_app`, `close_out_app`, and `clear_app` functions using the types of transaction application calls mentioned above.

Refer to this link for specific transaction calls for the application methods mentioned above: https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/.

Step 2: Implement `deploy_create_app`. First, compile the approval and clear state programs to TEAL assembly, then to binary. Create the application and the application arguments which should include a list of election parameters you defined previously as global variables: `election_end`, `num_vote_options`, `vote_options`.

Step 3: Implement the `main()` function where you initialize the algod client and define absolute election end time fom the status of the last round. Deploy the application and print the global state.

## Step 3 - Frontend Logic: `AlgoHandler.js`

If our frontend wants to display relevant information to our users it will need a way to retrieve data from the Algorand blockchain. Similarly, if our frontend wants to allow users to interact with our election smart contract our frontend will need to be able to send transactions to the Algorand blockchain. We will make use of the PureStake Algod client and Indexer client to retrieve information about the current state of our smart contract. We will use the AlgoSDK and AlgoSigner to create, sign, and send transactions to be added to the Algorand TestNet.

#### How

`frontend/src/components/AlgoHandler.js` is meant to contain all functionality related to retrieving information about the smart contract and sending transactions to the Algorand TestNet.

### Step 3.0 - Getting Familiar with the Tools

#### JavaScript

We do not assume that you have extensive knowledge about JavaScript. JavaScript is a very newcomer-friendly language that aligns nicely with other languages' syntax and paradigms. You will need to know variables, functions, loops, conditionals, and async/await in JavaScript. Here are some resources to get you started:

- [Learn javascript in Y Minutes](https://learnxinyminutes.com/docs/javascript/ "Learn javascript in Y Minutes") - basic JavaScript information
- [The await keyword](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await#the_await_keyword "The await keyword") - Essentially all you need to know about async/await for this homework
- Google - We highly encourage you to search for documentation, tutorials, and other resources if you would like to know more about any functionality or design patterns in JavaScript (how to iterate through an array, ternary operations, etc)

#### AlgoSDK

In Practical Homework 1 and parts of this homework you have used the Python version of the AlgoSDK. The frontend will make use of the JavaScript version of the AlgoSDK. Both versions are very similar in functionality and even close in syntax.

Take a look at the documentation here for how the Javscript AlgoSDK interacts with smart contracts:

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

#### AlgoHandler.js `frontend/src/components/AlgoHandler.js`

This file exports a singular instance of the class it contains which is meant to encapsulate data retrieval and transaction-sending from and to the Algorand blockchain.

We provide you a skeleton outline with all the necessary functions needed for you to fill out. You will be graded on producing the correct outputs for these functions (for those that have a specified return) and for sending the correct properly-formatted transactions (for those that require sending a transaction) .

### Step 3.1 - AlgoHandler constructor

In `frontend/src/components/AlgoHandler.js` fill out the `TODO` sections. Remember, don't change the variable names. You can define additional variables if needed.

- Set the `this.algodClient` variable
- Set the `this.indexerClient` variable

### Step 3.2 - Retrieving Data

In `frontend/src/components/AlgoHandler.js` fill out the following 4 functions with the commented functionality. Remember, don't change the function names. Feel free to add helper functions if you want. Remember to use JavaScript's `await` keyword when using `this.algodClient`, `this.algodIndexer`, and `window.AlgoSigner`

#### Relevant Documentation

- https://developer.algorand.org/solutions/example-digital-exchange-smart-contract-application/
- https://github.com/PureStake/algosigner/blob/develop/docs/dApp-integration.md#algosignerconnect

1.  `getAlgoSignerAccounts()`
    - **TODO:** Connect to AlgoSigner
    - **TODO:** Retrieve all addresses in array format and return them
2.  `isCreator(appID, address)`
    - **TODO:** Return a boolean based on if the given `address` is the creator of the app at `appID`
    - **HINT:** Two possible approaches are given in the code comments
3.  `getElectionState(appID)`
    - **TODO:** Use `this.algodClient` to retrieve the app details
    - The rest is filled out for you :)
4.  `getAllLocalStates(appID)`
    - **TODO:** Use `this.indexerClient` to find all accounts who are associated with the given app
    - **TODO:** Take the data and format it into a neat JavaScript object (nearly equivalent to a Python dictionary) as specified
      - Example:
      ```
        {
          'jsdalkfjsd...': {
            'can_vote': 'yes',
            'voted': 2
          },
          'fdsfdsaf...': {
            'can_vote': 'no'
          },
          'asdffdsaf...': {
            'can_vote': 'maybe'
          }
        }
      ```
      - **Note:** Only include values that are included in the original object. If a user does not have a value for `voted` then don't include the `voted` variable

### Step 3.3 - Sending Transactions

In `frontend/src/components/AlgoHandler.js` fill out the following 6 functions with the commented functionality. Remember, don't change the function names. Feel free to add helper functions if you want. Remember to use JavaScript's `await` when using `this.algodClient`, `this.algodIndexer`, and `window.AlgoSigner`

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
    - **TODO:** Set up the transaction app arguments
    - **TODO:** Create the transaction
      - Include both the creator's address and user's address in the optional address array when creating the transaction (different from app args)
    - **TODO:** Sign and send the transaction with our `this.signAndSend` function
4.  `vote(address, optionIndex, appID)`
    - **TODO:** Create app parameters, create transaction, sign and send
5.  `closeOut(address, appID)`
    - **TODO:** Create transaction, sign and send, similar to above
6.  `clearState(address, appID)`
    - **TODO:** Create transaction, sign and send, similar to above

## Step 4 - Implement the React front end

To use our application, we could write scripts to interact with the blockchain, but it is much easier to interact with a nice user interface. So, we will be connecting our blockchain to a React frontend to interact with the blockchain!

#### A brief tour of our React application

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

We highly recommend taking a look at how the components interact and how values are passed between the components, so that you have a good sense of how the frontend works when filling out the functions!

### Step 4.0 - Retrieve State from Blockchain

First, you should implement the `refreshState()` function in the `frontend/src/pages/ElectionPage.js`. Remember, don't change the function names. Remember to use the functions you have written in `AlgoHandler`!

- **TODO:** Get and update global election states (`electionState`, `totalVotes`, and `electionChoices`)
- **TODO:** Get and update local election states (`optedAccounts`, `userVotes`)

### Step 4.1 - Allow Users to Participate in Election

In the `frontend/src/components/VoteCard.js`, you will find 4 functions to implement. Remember to use the functions you have written in `AlgoHandler`!

1. `handleVoteSubmit()`

- **TODO:** Retrieve the vote from the form and send the vote to the blockchain

2. `handleOptIn()`

- **TODO:** Send a transaction to opt in user to the election

3. `handleCloseOut()`

- **TODO:** Send a transaction to close out the user from the election

4. `handleClearState()`

- **TODO:** Send a transaction to clear the user's vote from the election

### Step 4.2 - Allow Creator to Accept/Reject Users

In the `frontend/src/components/ParticipantsCard.js`, you will find 2 functions to implement. Remember to use the functions you have written in `AlgoHandler`!

1. `handleAccept()`

- **TODO:** Have the creator accept the user into the election

2. `handleReject()`

- **TODO:** Have the creator reject the user from the election

### Step 4.3 - Run application

Now, you have finished your application! You can try running the app in your Chrome browser by running `npm start` in the `frontend/voting-app` folder.
