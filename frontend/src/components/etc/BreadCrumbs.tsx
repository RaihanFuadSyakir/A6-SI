import Breadcrumbs from '@mui/material/Breadcrumbs'
import Link from '@mui/material/Link'
import Typography from '@mui/material/Typography'
import React from 'react'

export default function BreadCrumbs({path} :{path : string}) {
const parts = path.split('/');
  return (
    <Breadcrumbs aria-label="breadcrumb">
    {parts && parts.map((pth,index,array)=>{
        if(index === array.length-1){
        return <Typography color="text.primary">{pth}</Typography>
        }
        else if(index === 0){
            return <Link underline="hover" color="inherit" href="/home">Dashboard</Link>
        }
        else{
            return <Link underline="hover" color="inherit" href="/">{pth}</Link>
        }
    })
    }
    </Breadcrumbs>
  )
}
