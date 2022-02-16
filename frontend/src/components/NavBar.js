import React from "react";
import {
  Navbar,
  Container,
  DropdownButton,
  Dropdown,
  Button,
} from "react-bootstrap";

/*
 * Props:
 *  - connected (boolean): true if the user is connected to AlgoSigner
 *  - handlerUserUpdate (function): handles behavior when the user dropdown selection changes
 *  - accounts (list of strings): user addresses that are connected to AlgoSigner
 *  - mainAccount (string): user that is the current selection in the dropdown
 *  - refreshState (function): handles behavior when refresh button is clicked
 */
function NavBar(props) {
  /*
   * Render the navigation bar at the top of the page. It displays the logo ("AlgoVoter"),
   * a dropdown button to choose the account to work with, and a refresh button.
   */
  return (
    <Navbar
      style={{ backgroundColor: "#201f48" }}
      className="justify-content-end"
    >
      <Container>
        <Navbar.Brand style={{ color: "#0dcaf0", fontSize: "30px" }} href="/">
          AlgoVoter
        </Navbar.Brand>

        <Navbar.Collapse className="justify-content-end">
          {props.connected && props.accounts.length > 0 && (
            <DropdownButton
              variant="info"
              id="choose-user"
              title={props.mainAccount ? props.mainAccount : ""}
              className="px-3"
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
          {props.connected && (
            <Button variant="info" onClick={props.refreshState}>
              Refresh
            </Button>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
