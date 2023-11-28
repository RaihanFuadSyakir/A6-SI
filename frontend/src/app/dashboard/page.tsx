import LatestSyncPost from '@/components/post/LatestSyncPost'
import Button from '@mui/material/Button'
import React from 'react'
import GroupIcon from '@mui/icons-material/Group';
export default function Dashboard() {
  return (
    <div className='flex items-center justify-center h-auto'>
      <div className='flex flex-col'>
      <Button variant="contained" endIcon={<GroupIcon />} href='/users' className='bg-blue-600 hover:bg-blue-500'>
        List of Stored users
      </Button>
        <div className='flex justify-center'>Latest Sync Post</div>
        <LatestSyncPost/>
      </div>
      
    </div>
  )
}
