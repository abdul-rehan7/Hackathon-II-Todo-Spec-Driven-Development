import { NextResponse } from 'next/server';

export async function POST(request) {
  // Construct the backend URL using environment variable
  const backendUrl = `${process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000/api/v1'}/auth/logout`;

  try {
    // Get authorization header if present
    const authHeader = request.headers.get('authorization');

    console.log('Forwarding logout request to:', backendUrl); // Debug log
    console.log('Authorization header:', authHeader); // Debug log

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        ...(authHeader ? { 'authorization': authHeader } : {}),
        'Content-Type': 'application/json',
      },
    });

    console.log('Backend logout response status:', response.status); // Debug log

    const data = await response.json();

    console.log('Backend logout response data:', data); // Debug log

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy logout error:', error);
    return NextResponse.json({ error: 'Backend logout request failed', details: error.message }, { status: 500 });
  }
}