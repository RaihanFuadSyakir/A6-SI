"use client"
import Breadcrumbs from '@mui/material/Breadcrumbs'
import Link from '@mui/material/Link'
import Typography from '@mui/material/Typography'
import React from 'react'
import { usePathname } from 'next/navigation'
export default function BreadCrumbs() {
const pathname = usePathname();
const parts = pathname.split('/');
  return (
    <Breadcrumbs aria-label="breadcrumb">
    {parts && parts.map((pth,index,array)=>{
        if(index === array.length-1){
        return <Typography color="text.primary" key={index}>{pth}</Typography>
        }
        else if(index === 0){
            return <Link underline="hover" color="inherit" href="/dashboard" key={index}>~</Link>
        }
        else if(array.length > 2){
            return <Link underline="hover" color="inherit" href={`/${pth}`} key={index}>{pth}</Link>
        }
    })
    }
    </Breadcrumbs>
  )
}
