import React from 'react';
import {Link} from 'react-router-dom';
import {Navbar,Nav} from 'react-bootstrap';



export function Navigation() {
    {
        return(
            <Navbar bg="dark" expand="lg" id="my-nav">
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav>
                    <Link className="d-inline p-2 bg-dark text-white" to="/">
                        Home
                    </Link>

                    <Link className="d-inline p-2 bg-dark text-white" to="/student">
                        List Student
                    </Link>

                    <Link className="d-inline p-2 bg-dark text-white" to="/manage">
                        Manage Student
                    </Link>
                   
               </Nav>
                </Navbar.Collapse>

            </Navbar>
        )
    }
}
