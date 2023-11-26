"use client"
import BreadCrumbs from '@/components/etc/BreadCrumbs';
import UserProfile from '@/components/user/UserProfile'

import React from 'react'

export default function User({ params }: { params: { slug: string }}) {
  return (
    <div>
        <UserProfile username={params.slug}/>
    </div>
  )
}
