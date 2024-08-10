import React, { useEffect, useState } from "react"; 
import { Link } from "react-router-dom";
import axios from 'axios';

//TO DO LIST for Receipt 
/* 
    1. Design the Receipt Page 
    2. Build the functionality of the Table
    3. Retrieve the Data from the GUI Containerization
    4. Print out the Data from GUI Containerization:
        - Order ID
        - Customer ID
        - Customer First Name
        - Purchase Date 
        - Total 
*/

const API_URL = 'http://127.0.0.1:8000/backend/guitable/'

// This date and time have to be outside of the function 
// because we want these timeStamp to be static 
// if we put it in the function, then it will dynamically updated
//Get date
const today = new Date(); 
const month = today.getMonth()+1; 
const year = today.getFullYear();
const date = today.getDate(); 
const currentDate = month + "/" + date + "/" + year; 

//Get time
const hour = today.getHours(); 
const minute = today.getMinutes();
const second = today.getSeconds(); 
const currentTime = hour + ":" + minute + ":" + second; 

const Receipt = ()  => { 

    let total = 0.0;

    //At the beginning, data is an empty array 
    const [posts, setPosts] = useState([]);

    //At the beginning, total is 0 
    const [totalprice, setTotal] = useState(0.0);

    //define the function that fetches the data from API 
    const fetchData = async () => {
        // "data" => use this name specifically 
        // otherwise it causes problem 
        const { data } = await axios.get(API_URL);
        setPosts(data);
    }

    //defin the function that add up the total price based on the subtotal
    const changeTotalPrice = async () => {
        //use data (posts) and iterate thru using map to get the subtotal
        posts.map((post) => (
            total += post.subtotal
        ))

        setTotal(total.toFixed(2)); //set to 2 decimal places
        //reset total to 0, otherwise it keeps adding up 
        total = 0.0;
    }

    //trigger the fetchData after the initial render by using the useEffect hook
    useEffect(() => {
        fetchData(); // fetch data initially
        changeTotalPrice(); //fetch totalprice initially

    }, [posts, totalprice]); // add these variables to perform an action on state update 
                            // otherwise it won't take update action 



    return (
        <div>
            {/* Align to the center of the page */}
            <h1 className="receipt_title">Receipt</h1>  
            
            <div className="store_address">
                <h2 className="logo">Logo</h2>
                <h3 className="store_name">Smart Cart</h3>
                <h6>University of California Irvine</h6>
                <h6>Irvine, CA 92697</h6>
            </div>
            
            {/* These ID and name are align to the left */}
            <div className="info">
            <div>Order ID: <span id="box">id in the box</span></div>
            <div>Customer ID: <span id="box">id in the box</span></div>
            <div>Customer First Name: <span id="box">name in the box</span></div>
            </div>
            
            {/* This table is align at the left  */}
            <table id="receipt_table">
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

            {/* Purchase Date aligns to the left */}
            <p id="date">Purchase Date: <span id="current_date">{currentDate}  {currentTime}</span></p>
            {/* Total aligns to the right */}
            <p id="total">Total: <span id="total_price">$ {totalprice}</span></p>
            <Link to="/"><button className="page_button home_button">Return To Home</button></Link>
        </div>
        
        
    );
}


export {Receipt}; 
