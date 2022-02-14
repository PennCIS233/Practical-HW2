import React, { useState } from "react";
import { Card, Button, Form } from "react-bootstrap";
import mainAlgoHandler from "../components/AlgoHandler";

function VoterCard(props) {
  const [voteChoice, setVoteChoice] = useState("");

  // handleVoteSelect
  // Description:
  //  Updates the states when the user changes their vote option
  const handleVoteSelect = (e) => {
    setVoteChoice(e.target.value);
  };

  // handleVoteSubmit
  // Description:
  //  Sends the vote to the blockchain.
  const handleVoteSubmit = (e) => {
    // TODO: connect to AlgoHandler
  };

  // handleOptIn
  // Description:
  //  Opts the user into the election on the blockchain.
  const handleOptIn = (e) => {
    // TODO: connect to AlgoHandler
  };

  // handleClear
  // Description:
  //  Clears the user vote on the blockchain.
  const handleClear = (e) => {
    // TODO: connect to AlgoHandler
  };

  return (
    <Card>
      {!props.isOpted && !props.isAccepted && !props.isRejected && (
        <Card.Body>
          <Card.Title>Opt In to the Election</Card.Title>
          <Card.Text>
            To participate in the election, you must opt-in. If the creator of
            the election accepts, you can vote!
          </Card.Text>
          <Form onSubmit={handleOptIn}>
            <Button variant="info" type="submit">
              Opt-In
            </Button>
          </Form>
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
            <Form onSubmit={handleVoteSubmit}>
              <Form.Group controlId="vote-options">
                {props.electionChoices.map((choice) => (
                  <Form.Check
                    type="radio"
                    key={choice}
                    value={choice}
                    name="choices"
                    label={choice}
                    onChange={handleVoteSelect}
                  />
                ))}
              </Form.Group>
              <Button variant="info" type="submit">
                Vote
              </Button>
            </Form>
          </Card.Body>
        </div>
      )}

      {props.isVoted !== undefined && (
        <Card.Body>
          <Card.Title>You Voted!</Card.Title>
          <Card.Text>
            You have cast your vote for option{" "}
            {props.electionChoices[props.isVoted]}
          </Card.Text>
        </Card.Body>
      )}

      {props.isRejected && (
        <Card.Body>
          <Card.Title>You Have Been Rejected</Card.Title>
          <Card.Text>
            The creator of this election has rejected your request to be able to vote in this election
          </Card.Text>
          <Form onSubmit={handleCloseOut}>
            <Button variant="info" type="submit">
              Close Out
            </Button>
          </Form>
          <Form onSubmit={handleClearState}>
            <Button variant="info" type="submit">
              Clear State
            </Button>
          </Form>
        </Card.Body>
      )}
    </Card>
  );
}

export default VoterCard;
