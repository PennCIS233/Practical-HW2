import React from "react";
import {
  Card,
  Button,
  Accordion,
  Tabs,
  Tab,
  ButtonGroup,
} from "react-bootstrap";
import mainAlgoHandler from "./AlgoHandler";

/*
 * Props:
 *  - appID (string): id of the election
 *  - users (list of strings): user addresses that are connected to AlgoSigner
 *  - user (string): user that is the current selection in the dropdown
 *  - isCreator (boolean): true if the current user is the creator of the election
 *  - optedAccounts (JSON of lists of strings) - lists of users that are accepted, rejected and pending
 *  - electionChoices (string) - comma-separated string of the election choices
 */
function ParticipantsCard(props) {
  /* handleAccept
   * Description:
   *   Makes call to approve a user when 'Accept' button is pressed
   * Parameters:
   *  user (string) - user to accept into the election
   */
  const handleAccept = (user) => {
    mainAlgoHandler.updateUserStatus(
      props.user,
      user,
      "yes",
      parseInt(props.appID)
    );
  };

  /* handleReject
   * Description:
   *  Makes call to approve a user when 'Reject' button is pressed
   * Parameters:
   *  user (string) - user to reject from the election
   */
  const handleReject = (user) => {
    mainAlgoHandler.updateUserStatus(
      props.user,
      user,
      "no",
      parseInt(props.appID)
    );
  };

  /*
   * Render a card containing three tabs - "Accepted", "Rejected", and "Pending". All tabs
   * contain a list of Accordions that allow the user to click and view more information about
   * any user that has opted-in to the election. If the user is the creator, they can accept/reject
   * users in the "Pending" tab.
   */
  return (
    <Card className="h-50">
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
                      <b>User Address:</b> {user}
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
                    <Accordion.Body>
                      <b>User Address:</b> {user}
                    </Accordion.Body>
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
                      <b>User Address:</b> {user}
                      {props.isCreator && (
                        <div>
                          <ButtonGroup className="mt-1">
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
                          </ButtonGroup>
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
