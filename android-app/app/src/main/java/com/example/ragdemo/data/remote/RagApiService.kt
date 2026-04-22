package com.example.ragdemo.data.remote

import com.example.ragdemo.data.model.RagRequest
import com.example.ragdemo.data.model.RagResponse
import retrofit2.http.Body
import retrofit2.http.POST

interface RagApiService {
    @POST("ask")
    suspend fun askQuestion(@Body request: RagRequest): RagResponse
}
