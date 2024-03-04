"use client";

import React, { useState } from 'react';
import { useSession } from "next-auth/react";


const MyPage = () => {
  const [responseData, setResponseData] = useState(null);
  const {data: session} = useSession()

  const fetchData = async () => {
    try {
      const response = await fetch('http://175.194.198.155:8080/user/me', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${session.access_token}`
        }
        // You can include additional options here if needed
      });

      if (response.ok) {
        const res = await response.json();
        setResponseData(res);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };


  return (
    <div>
      <h1>My Page</h1>
      <p>This is my page</p>
      <button onClick={fetchData}>Fetch Data</button>
      {responseData && (
        <div>
          <h2>Response Data:</h2>
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default MyPage;
