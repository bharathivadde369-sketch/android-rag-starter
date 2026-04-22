package com.example.ragdemo.data.repository

import com.example.ragdemo.data.model.RagRequest
import com.example.ragdemo.data.model.RagResponse
import com.example.ragdemo.data.remote.RagApiService

class RagRepository(
    private val apiService: RagApiService
) {
    suspend fun ask(query: String): Result<RagResponse> {
        return try {
            Result.success(apiService.askQuestion(RagRequest(query)))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
