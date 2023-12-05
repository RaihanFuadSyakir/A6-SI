"use client"
import { User, UserLogin, axiosInstance, jsonFormat } from '@/utils/DataFetching';
import { AxiosError, AxiosResponse } from 'axios';
import React, { useEffect, useState } from 'react'
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
export default function LoginUser() {
    const[isLogged,setLogged] = useState(true);
    const[username,setUsername] = useState('')
    const[password,setPassword] = useState('')
    const handleLogin = () => {
        axiosInstance.post('/user_login',{
            "username":username,
            "password":password
        })
        .then((res:AxiosResponse<jsonFormat<UserLogin>>)=>{
            setLogged(res.data.data.is_logged)
        })
        .catch((err_res:AxiosError<jsonFormat<UserLogin>>)=>{
            console.log(JSON.stringify(err_res.response?.data))
        })
      };
    useEffect(()=>{
        axiosInstance.get('/get_login_state')
        .then((res:AxiosResponse<jsonFormat<UserLogin>>)=>{
            setLogged(res.data.data.is_logged);
        })
        .catch((err_res:AxiosError<jsonFormat<UserLogin>>)=>{
            console.log(JSON.stringify(err_res.response?.data.data))
        })
    },[])
  return (
    <div className='w1/4 m-4'>
        {isLogged ? (
            <div>Logged in</div>
            ) :
            (<div className='flex flex-col'>
                <TextField
                    label="Username"
                    variant="outlined"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Password"
                    type="password"
                    variant="outlined"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    fullWidth
                    margin="normal"
                />
                <Button variant="contained" color="primary" onClick={handleLogin} className={`bg-blue-600 hover:bg-blue-500`}>
                    Login
                </Button>
            </div>)
        }
    </div>
  )
}
