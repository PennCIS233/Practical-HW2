import React from "react";
import { Card, Button, Accordion, Tabs, Tab } from "react-bootstrap";
import mainAlgoHandler from "./AlgoHandler";

function ParticipantsCard(props) {
  // handleAccept
  // Description:
  //  Makes call to approve a user when 'Accept' button is pressed
  // Parameters:
  //  user (string) - user to accept into the election
  const handleAccept = (user) => {
    // TODO: connect this function to AlgoHandler
  };

  // handleReject
  // Description:
  //  Makes call to approve a user when 'Reject' button is pressed
  // Parameters:
  //  user (string) - user to reject from the election
  const handleReject = (user) => {
    // TODO: connect this function to AlgoHandler
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>Opted In Users</Card.Title>
        <Tabs
          defaultActiveKey="Accepted"
          id="uncontrolled-tab-example"
          className="mb-3"
        >
          <Tab
            eventKey="Accepted"
            title={`Accepted (${props.optedAccounts["yes"].length})`}
          >
            <Accordion>
              {props.optedAccounts["yes"] &&
                props.optedAccounts["yes"].map((user) => (
                  <Accordion.Item eventKey={user} key={`yes-${user}`}>
                    <Accordion.Header>
                      {user.substring(0, 20) + "..."}
                    </Accordion.Header>
                    <Accordion.Body>
                      <b>Creator:</b> {user}
                      <br />
                      {props.electionChoices[props.userVotes[user]] && (
                        <div>
                          <b>Vote:</b>{" "}
                          {props.electionChoices[props.userVotes[user]]}{" "}
                        </div>
                      )}
                    </Accordion.Body>
                  </Accordion.Item>
                ))}
            </Accordion>
          </Tab>
          <Tab
            eventKey="Rejected"
            title={`Rejected (${props.optedAccounts["no"].length})`}
          >
            <Accordion>
              {props.optedAccounts["no"] &&
                props.optedAccounts["no"].map((user) => (
                  <Accordion.Item eventKey={user} key={`no-${user}`}>
                    <Accordion.Header>
                      {user.substring(0, 20) + "..."}
                    </Accordion.Header>
                    <Accordion.Body>Creator: {user}</Accordion.Body>
                  </Accordion.Item>
                ))}
            </Accordion>
          </Tab>
          <Tab
            eventKey="Opted-In"
            title={`Pending (${props.optedAccounts["maybe"].length})`}
          >
            <Accordion>
              {props.optedAccounts["maybe"] &&
                props.optedAccounts["maybe"].map((user) => (
                  <Accordion.Item eventKey={user} key={`maybe-${user}`}>
                    <Accordion.Header>
                      {user.substring(0, 20) + "..."}
                    </Accordion.Header>
                    <Accordion.Body>
                      Creator: {user}
                      {props.isCreator && (
                        <div>
                          <Button
                            onClick={() => handleAccept(user)}
                            variant="success"
                          >
                            Accept
                          </Button>
                          <Button
                            onClick={() => handleReject(user)}
                            variant="danger"
                          >
                            Reject
                          </Button>
                        </div>
                      )}
                    </Accordion.Body>
                  </Accordion.Item>
                ))}
            </Accordion>
          </Tab>
        </Tabs>
      </Card.Body>
    </Card>
  );
}

export default ParticipantsCard;
