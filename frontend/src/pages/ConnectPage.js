import React, { useState } from "react";
import { Row, Col, Card, Container, Button, Form } from "react-bootstrap";
import mainAlgoHandler from "../utils/AlgoHandler";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";

function ConnectPage() {
  /*
   * Navigate lets us pass stateto the ElectionPage component.
   */
  let navigate = useNavigate();

  /*
   * Here we define the stored state for this component.
   */
  const [accounts, setAccounts] = useState([]); // list of user addresses connected to AlgoSigner
  const [isConnected, setIsConnected] = useState(false); // boolean that is true if the page is connected to AlgoSigner

  /* connectAlgoSigner
   * Description:
   * retrieves the user accounts from AlgoSigner
   */
  const connectAlgoSigner = async () => {
    let newAccounts = await mainAlgoHandler.getAlgoSignerAccounts();
    setAccounts(newAccounts);
    setIsConnected(true);
  };

  /* handleElectionSubmit
   * Description:
   *  takes the value inputted into the appID form and naviagates to ElectionPage,
   *  sending along the relevant state (accounts and appID)
   * */
  const handleElectionSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formDataObj = Object.fromEntries(formData.entries());
    console.log(formDataObj);
    navigate("/election", {
      state: { accts: accounts, appID: formDataObj["appID"] },
    });
  };

  /*
   * Render the connect page. It displays the NavBar at the top of the page,
   * as well as a button to connect to AlgoSigner and a form to fill in the app ID.
   */
  return (
    <>
      <NavBar />
      <Container>
        <Row className="px-3 mt-3">
          <Col>
            <Card className="mt-5">
              <Card.Body>
                <Card.Title>Connect to AlgoSigner</Card.Title>
                <Button variant="info" onClick={connectAlgoSigner}>
                  Connect
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
      <Container>
        <Row className="px-3 mt-3">
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>App ID</Card.Title>
                <Form onSubmit={async (e) => await handleElectionSubmit(e)}>
                  <Form.Group className="mb-3" controlId="appID">
                    <Form.Control
                      disabled={!isConnected}
                      type="election"
                      name="appID"
                      placeholder="Enter app id"
                    />
                  </Form.Group>
                  <Button variant="info" type="submit">
                    Submit
                  </Button>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default ConnectPage;
