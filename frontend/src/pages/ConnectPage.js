import React, { useState } from "react";
import { Row, Col, Card, Container, Button, Form } from "react-bootstrap";
import mainAlgoHandler from "../components/AlgoHandler";
import NavBar from "../components/NavBar";
import { useNavigate } from "react-router-dom";

function ConnectPage() {
  const [accounts, setAccounts] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  let navigate = useNavigate();

  // connectAlgoSigner
  // Description:
  // retrieves the user accounts from AlgoSigner
  const connectAlgoSigner = async () => {
    let newAccounts = await mainAlgoHandler.getAlgoSignerAccounts();
    setAccounts(newAccounts);
    setIsConnected(true);
  };

  // handleElectionSubmit
  // Description:
  // takes the value inputted into the appID form and
  // naviagates to the election page
  const handleElectionSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formDataObj = Object.fromEntries(formData.entries());
    console.log(formDataObj);
    navigate("/election", {
      state: { accts: accounts, appID: formDataObj["appID"] },
    });
  };

  return (
    <>
      <NavBar />
      <Container>
        <Row className="px-3 mt-3">
          <Row>
            <Col>
              <Card className="mt-5">
                <Card.Body>
                  <Card.Title>Connect to AlgoSigner</Card.Title>
                  <Button
                    variant="info"
                    onClick={connectAlgoSigner}
                    disabled={isConnected}
                  >
                    Connect
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Row>
      </Container>
      <Container>
        <Row className="px-3 mt-3">
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Election ID</Card.Title>
                <Form onSubmit={async (e) => await handleElectionSubmit(e)}>
                  <Form.Group className="mb-3" controlId="appID">
                    <Form.Control
                      disabled={!isConnected}
                      type="election"
                      name="appID"
                      placeholder="Enter election id"
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
