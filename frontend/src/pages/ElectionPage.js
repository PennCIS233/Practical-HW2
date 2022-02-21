import React, { useEffect, useState } from "react";
import { Row, Col, Container, Modal, Button } from "react-bootstrap";
import mainAlgoHandler from "../utils/AlgoHandler";
import NavBar from "../components/NavBar";
import VoterCard from "../components/VoterCard";
import ParticipantsCard from "../components/ParticipantsCard";
import ElectionInfoCard from "../components/ElectionInfoCard";

import { useLocation } from "react-router-dom";

function ElectionPage() {
  /*
   * Location lets us access the state (appID and accounts) passed to the component from the ConnectPage.
   */
  let location = useLocation();
  const appID = location.state.appID; // appID that the user entered
  const accounts = location.state.accts; // accounts that are connected to AlgoSigner

  /*
   * Here we define the stored state for this component.
   */
  const [isError, setIsError] = useState(false); // boolean set to true if there is an error retrieving the electionState
  const [electionState, setElectionState] = useState({}); // JSON containing all global variables for the application
  const [mainAccount, setMainAccount] = useState(
    accounts.length > 0 ? accounts[0] : ""
  ); // string that is set to the current account
  const [totalVotes, setTotalVotes] = useState([]); // array of integers storing the total number of votes for each choice
  const [electionChoices, setElectionChoices] = useState([]); // array of strings listing the choices in the election
  const [userVotes, setUserVotes] = useState({}); // JSON containing a mapping of user addresses to their votes in the election
  const [optedAccounts, setOptedAccounts] = useState({
    maybe: [],
    yes: [],
    no: [],
  }); // JSON of lists containing the user addresses who have are accepted, rejected, and pending

  /* refreshState
   * Description:
   * Calls API to get election state and list of all users that have opted-in.
   */
  const refreshState = () => {
    console.log("refreshing state...");

    mainAlgoHandler
      .getElectionState(location.state.appID)
      .then((res) => {
        let newTotalVotes = [];
        for (let i = 0; i < res["NumVoteOptions"]; i++) {
          newTotalVotes.push(res[`VotesFor${i}`]);
        }

        let newElectionChoices = res["VoteOptions"].split(",");
        setElectionState(res);
        setTotalVotes(newTotalVotes);
        setElectionChoices(newElectionChoices);
      })
      .catch((err) => {
        console.log(err);
        setIsError(true);
      });

    console.log(electionState);

    mainAlgoHandler
      .getAllLocalStates(parseInt(appID))
      .then((allLocalStates) => {
        let newOptedAccounts = {
          yes: [],
          no: [],
          maybe: [],
        };
        for (const address in allLocalStates) {
          let canVote = allLocalStates[address]["can_vote"];
          if ("can_vote" in allLocalStates[address]) {
            newOptedAccounts[canVote].push(address);
          }
        }
        setOptedAccounts(newOptedAccounts);

        let newUserVotes = {};
        for (const address in allLocalStates) {
          if ("voted" in allLocalStates[address]) {
            newUserVotes[address] = allLocalStates[address]["voted"];
          }
        }
        setUserVotes(newUserVotes);
      })
      .catch((err) => {
        console.log(err);
        setIsError(true);
      });
  };

  /* useEffect
   * Description:
   *  Retrieves election state when component is first rendered
   */
  useEffect(() => {
    refreshState();
  }, []);

  /* handleMainAccountChange
   * Description:
   *  Updates the main account and updates the state
   * Parameters:
   *  user (string) - user to change main account to
   */
  const handleMainAccountChange = (user) => {
    setMainAccount(user);
    refreshState();
  };

  /*
   * Render the main election page. It displays the NavBar at the top of the page,
   * as well as three Cards - the global election info, the election participants,
   * and a form to participate in the election. If isError is true, then a Modal
   * (a popup) is displayed.
   */
  return (
    <>
      <NavBar
        connected
        handleUserUpdate={handleMainAccountChange}
        accounts={accounts}
        mainAccount={mainAccount}
        refreshState={refreshState}
      />
      <Container>
        <Row xs={1} md={2} className="g-4 mt-3">
          <Col>
            <ParticipantsCard
              appID={appID}
              users={accounts}
              user={mainAccount}
              userVotes={userVotes}
              isCreator={electionState["Creator"] === mainAccount}
              optedAccounts={optedAccounts}
              electionChoices={electionChoices}
            />
          </Col>

          <Col>
            <ElectionInfoCard
              currVotes={totalVotes}
              appID={appID}
              state={electionState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            {accounts.length > 0 && (
              <VoterCard
                user={mainAccount}
                appID={appID}
                electionState={electionState}
                isAccepted={optedAccounts["yes"].includes(mainAccount)}
                isPending={optedAccounts["maybe"].includes(mainAccount)}
                isRejected={optedAccounts["no"].includes(mainAccount)}
                isVoted={userVotes[mainAccount]}
                electionChoices={electionChoices}
              />
            )}
          </Col>
        </Row>
      </Container>
      <Modal show={isError}>
        <Modal.Header>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          There was an error when retrieving the application state. Please check
          that you entered the correct application ID.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="info" href="/">
            Return to Connect Page
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default ElectionPage;
