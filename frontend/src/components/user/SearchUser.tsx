"use client"
import React, { useState } from 'react'
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import PersonIcon from '@mui/icons-material/Person';
import { User, axiosInstance, jsonFormat } from '@/utils/DataFetching';
import { AxiosResponse } from 'axios';
interface setUser {
    users : User[];
    setUsers : React.Dispatch<React.SetStateAction<User[]>>;
  }
export default function SearchUser({users,setUsers} : setUser) {
    const [isLoading,setLoading] = useState(false);
    const [username,setUsername] = useState('');
    console.log(username);
    function inputOnChange(e : any){
        const value = e.target.value;
        setUsername(value);
    }
    function sync_user(e : any){
      setLoading(true);
      axiosInstance.post(`/sync_user/${username}`)
        .then((response : AxiosResponse<jsonFormat<User>>)=>{
          const newUser = response.data.data;
          const newUsers = [...users,newUser]
          setUsers(newUsers)
          setLoading(false);
        })
        .catch((err_response)=>{
          console.log(err_response)
          setLoading(false);
        })
    }
  return (
    <Paper
      component="form"
      sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 300 }}
    >
      <PersonIcon className='m-auto'/>
      <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder="Search User"
        inputProps={{ 'aria-label': 'Search User' }}
        onChange={inputOnChange}
      />
      <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={sync_user} disabled={isLoading}>
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}