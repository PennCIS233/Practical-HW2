import React, { useState } from "react";
import {
  ButtonGroup,
  Card,
  Button,
  DropdownButton,
  Dropdown,
} from "react-bootstrap";
import mainAlgoHandler from "../components/AlgoHandler";

/*
 * Props:
 *  - appID (string): id of the election
 *  - user (string): user that is the current selection in the dropdown
 *  - electionState (JSON): global state of the election
 *  - isAccepted (boolean): true if the user has been accepted
 *  - isPending (boolean): true if the user has opted-in but not been accepted/ rejected
 *  - isRejected (boolean): true if the user has been rejected
 *  - is Voted (boolean): true if the user has voted in the election already
 *  - electionChoices (string) - comma-separated string of the election choices
 */
function VoterCard(props) {
  const [voteChoice, setVoteChoice] = useState(""); // holds the vote option chosen on the radio select form

  /* handleVoteSelect
   * Description:
   *  Updates the states when the user changes their vote option
   */
  const handleVoteSelect = (choice) => {
    setVoteChoice(choice);
  };

  /* handleVoteSubmit
   * Description:
   *  Sends the vote to the blockchain.
   */
  const handleVoteSubmit = (e) => {
    e.preventDefault();
    const choices = props.electionChoices;
    let voteValue = choices.indexOf(voteChoice);
    if (voteValue > -1)
      mainAlgoHandler.vote(props.user, voteValue, parseInt(props.appID));
  };

  /* handleOptIn
   * Description:
   *  Opts the user into the election on the blockchain.
   * */
  const handleOptIn = (e) => {
    e.preventDefault();
    mainAlgoHandler.optInAccount(props.user, parseInt(props.appID));
  };

  /* handleClearState
   * Description:
   *  Clears the user vote on the blockchain.
   */
  const handleClearState = (e) => {
    e.preventDefault();
    mainAlgoHandler.clearState(props.user, parseInt(props.appID));
  };

  /* handleCloseOut
   *  Description:
   *   Closes out the user vote on the blockchain.
   */
  const handleCloseOut = (e) => {
    e.preventDefault();
    mainAlgoHandler.closeOut(props.user, parseInt(props.appID));
  };

  /*
   * Render the card which allows the user to participate in the election.
   * In the beginning, the user can opt-in, and then the card shows a page
   * which waits for acceptance. If the user is rejected, then they are done.
   * If they are accepted, they have the option to vote in the election. Once
   * they vote, they can clear state / close out.
   */
  return (
    <Card className="mt-4 mb-4 text-center">
      {!props.isPending && !props.isAccepted && !props.isRejected && (
        <Card.Body>
          <Card.Title>Opt-In to the Election</Card.Title>
          <Card.Text>
            To participate in the election, you must opt-in. If the creator of
            the election accepts, you can vote!
          </Card.Text>
          <Button variant="info" onClick={handleOptIn}>
            Opt-In
          </Button>
        </Card.Body>
      )}

      {props.isPending && (
        <Card.Body>
          <Card.Title>Waiting for Acceptance</Card.Title>
          <Card.Text>
            Waiting for the creator of the election to accept...
          </Card.Text>
        </Card.Body>
      )}

      {props.isAccepted && props.isVoted === undefined && (
        <div>
          <Card.Body>
            <Card.Title>Cast Your Vote</Card.Title>
            <Card.Text>Use the dropdown below to select your vote!</Card.Text>
            <ButtonGroup>
              <DropdownButton
                variant="info"
                title={`Option ${voteChoice}`}
                id="voteOptions"
              >
                {props.electionChoices.map((choice) => (
                  <Dropdown.Item
                    key={choice}
                    value={choice}
                    onClick={() => handleVoteSelect(choice)}
                  >
                    {choice}
                  </Dropdown.Item>
                ))}
              </DropdownButton>

              <Button variant="info" onClick={handleVoteSubmit}>
                Vote
              </Button>
            </ButtonGroup>
          </Card.Body>
        </div>
      )}

      {props.isVoted !== undefined && (
        <Card.Body>
          <Card.Title>You Voted!</Card.Title>
          <Card.Text>
            You have cast your vote for option{" "}
            {props.electionChoices[props.isVoted]}.
          </Card.Text>
          <Card.Text>
            If you'd like to have your vote removed, you can either close out or
            clear state below.
          </Card.Text>
          <ButtonGroup>
            <Button onClick={handleCloseOut} variant="info" type="submit">
              Close Out
            </Button>
            <Button onClick={handleClearState} variant="info" type="submit">
              Clear State
            </Button>
          </ButtonGroup>
        </Card.Body>
      )}

      {props.isRejected && (
        <Card.Body>
          <Card.Title>You Have Been Rejected</Card.Title>
          <Card.Text>
            The creator of this election has rejected your request to be able to
            vote in this election.
          </Card.Text>

          <ButtonGroup>
            <Button onClick={handleCloseOut} variant="info" type="submit">
              Close Out
            </Button>
            <Button onClick={handleClearState} variant="info" type="submit">
              Clear State
            </Button>
          </ButtonGroup>
        </Card.Body>
      )}
    </Card>
  );
}

export default VoterCard;
