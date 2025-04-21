import { NextResponse,NextRequest } from "next/server";

export async function POST(req:NextRequest) {
    const body = await req.json()
    const {name, email,password} = body

    const res = await fetch('http://localhost:8000/signup', {
     method: "POST",
     headers: {'Content-Type':"application/json"},
     body: JSON.stringify({name,email,password}),

    });

    const result = await res.json();

  return NextResponse.json({ message: result.message });
}

