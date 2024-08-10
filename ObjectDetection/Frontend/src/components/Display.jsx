import React, { useEffect, useState } from 'react'; 
import {Link} from "react-router-dom";
import axios from 'axios';
import Popup from "reactjs-popup"; 
// import { Table } from 'react-bootstrap'; 


const API_URL = 'http://127.0.0.1:8000/backend/guitable/'


const GUITable = () => {
    
    let total = 0.0; 

    //At the beginning, data is an empty array 
    const [posts, setPosts] = useState([]);

    //At the beginning, total is 0
    const [totalprice, setTotal] = useState(0.0);



    //define the function that add up the total price based on the subtotal
    
    const changeTotalPrice = async () => {
        
        //use data (posts) and iterate thru using map to get the subtotal 
        posts.map((post) => (
            total += post.subtotal
        ))
        
        setTotal(total.toFixed(2)); // set to 2 decimal places
        //reset total to 0, otherwise it keeps adding
        total = 0.0;
    }

    //define the function that fetches the data from API 
    const fetchData = async () => {
        // "data" => use this name specifically 
        // otherwise it causes problem 
        const { data } = await axios.get(API_URL);
        setPosts(data);   
    }
 
    //trigger the fetchData after the initial render by using the useEffect hook
    useEffect(() => {
        fetchData(); // fetch data initially
        changeTotalPrice(); // fetch totalprice initially
        // intervalID stores a variable so that it can be cleared after new fetch
        const intervalID = setInterval(() => {
            fetchData(); // function #1
            changeTotalPrice(); // function #2
        }, 4000); //auto fetch every 4 sec. ==> 1 sec = 1000 
                // intervalID stores a variable so that it can be cleared after new fetch 

        return () => clearInterval(intervalID); //clear the previous intervalID 
    
    }, [posts, totalprice]); // add these variables to perform an action on state update 
                            // otherwise it won't take update action 

    return (
        <div className="background">
            <h1 className="gui_title">Item In Cart</h1>
            <table id="gui_table">
                <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Unit</th>
                    <th>Price Per Unit</th>
                    <th>Subtotal</th>
                </tr>

            {posts.length > 0 ? (
                <tbody>
                    {posts.map((post) => (
                    <tr>   
                        <td>{post.product_id}</td>
                        <td>{post.product_name}</td>
                        <td>{post.unit}</td>
                        <td>{post.price_per_unit}</td>
                        <td>{post.subtotal}</td>
                    </tr> 
                    ))}
                </tbody>        
            ): (
            <p className = 'loading'>Loading...</p>
        )}
                
    </table>  

    <div><p id="total">Total: <span id="total_price">$ {totalprice}</span></p></div>   
    <div>
        <Popup 
            trigger={<button className="page_button">DONE SHOPPING</button>}
            position="left center"> 
            <Link to="/PayProcess"><button >Proceed to Checkout</button></Link>

        </Popup>
    </div>   
    {/* <div><Link to="/prompt"><button className="page_button">DONE SHOPPING</button></Link></div> */}

        </div>
    );
};
    
export {GUITable};