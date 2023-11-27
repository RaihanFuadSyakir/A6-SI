"use client"
import { DataProgress, User, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosResponse } from 'axios'
import Image from 'next/image'
import { ChangeEvent, useEffect, useState } from 'react'
import SyncIcon from '@mui/icons-material/Sync';
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';
interface setUser {
  users : User[];
  setUsers : React.Dispatch<React.SetStateAction<User[]>>;
  index : number;
}
export default function SyncUser({users,setUsers, index} : setUser) {
  const [isSync,setSync] = useState(false);
    function sync_user(e : any){
      setSync(true);
      axiosInstance.post(`/sync_user/${users[index].username}`)
        .then((response : AxiosResponse<jsonFormat<User>>)=>{
          const newUser = response.data.data;
          const newUsers = [...users]
          newUsers[index] = newUser;
          setUsers(newUsers)
          setSync(false);
        })
        .catch((err_response)=>{
          console.log(err_response)
        })
    }
    return (
      <IconButton color="primary" aria-label="sync" className={`rounded-full hover:bg-sky-300`} onClick={sync_user}>
        {isSync ? (<CircularProgress />):(<SyncIcon/>)}
      </IconButton>
      
    )
}
