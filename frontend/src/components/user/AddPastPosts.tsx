"use client"
import { User, axiosInstance, jsonFormat } from '@/utils/DataFetching'
import { AxiosResponse } from 'axios'
import { ChangeEvent, useEffect, useState } from 'react'
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';
import AddIcon from '@mui/icons-material/Add';
interface setUser {
  users : User[];
  setUsers : React.Dispatch<React.SetStateAction<User[]>>;
  index : number;
}
export default function AddPastPosts({users,setUsers, index} : setUser) {
  const [isSync,setSync] = useState(false);
    function sync_user(e : any){
      setSync(true);
      axiosInstance.post(`/get_past_posts/${users[index].username}`)
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
        {isSync ? (<CircularProgress />):(<AddIcon/>)}
      </IconButton>
      
    )
}
