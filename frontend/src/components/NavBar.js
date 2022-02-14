import React from "react";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { DropdownButton, Dropdown, Button } from "react-bootstrap";

function NavBar(props) {
  return (
    <Navbar style={{ backgroundColor: "#201f48" }}>
      <Container>
        <div>
          <Navbar.Brand style={{ color: "#0dcaf0", fontSize: "30px" }} href="/">
            AlgoVoter
          </Navbar.Brand>
          {props.connected && (
            <Button variant="info" onClick={props.refreshState}>
              Refresh
            </Button>
          )}
        </div>
        {props.connected && (
          <DropdownButton
            variant="info"
            id="choose-user"
            title={props.mainAccount ? props.mainAccount : ""}
          >
            {props.accounts.map((user) => (
              <Dropdown.Item
                key={user}
                onClick={() => props.handleUserUpdate(user)}
              >
                {user}
              </Dropdown.Item>
            ))}
          </DropdownButton>
        )}
      </Container>
    </Navbar>
  );
}

export default NavBar;
