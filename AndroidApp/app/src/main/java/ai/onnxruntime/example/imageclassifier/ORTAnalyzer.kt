// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

package com.ballers.tracer

import ai.onnxruntime.*
import android.graphics.Bitmap
import android.graphics.Matrix
import android.os.SystemClock
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import java.util.*
import kotlin.math.exp


internal data class Result(
        var detectedIndices: MutableList<Int> = mutableListOf(),
        var detectedScore: MutableList<Float> = mutableListOf(),
        var processTimeMs: Long = 0
) {}

internal class ORTAnalyzer(
        private val ortSession: OrtSession?,
        private val callBack: (Result) -> Unit
) : ImageAnalysis.Analyzer {

    // Get index of top 3 values
    // This is for demo purpose only, there are more efficient algorithms for topK problems
    private fun getTop3(foundObjects: List<ClassifiedBox>): List<ClassifiedBox> {
        return foundObjects.sortedByDescending { it.confidence }.take(3)
    }

    private val CONFIDENCE_THRESHOLD: Float = 0.3F
    private val SCORE_THRESHOLD: Float = 0.2F
    private val IMAGE_WIDTH: Float = 640.0F
    private val IMAGE_HEIGHT: Float = 640.0F

    data class ClassifiedBox(
        val centerX: Float,
        val centerY: Float,
        val width: Float,
        val height: Float,
        val classId: Int,
        val confidence: Float
    )

    private fun getIndOfMaxValue(classesScore: List<Float>): Int {
        var ind = 0
        for (i in 1 until classesScore.size) {
            if (classesScore[i] > classesScore[ind]) {
                ind = i
            }
        }
        return ind
    }

    // That function parses the yolov5 model output.
    // I assumed the format from this project https://github.com/doleron/yolov5-opencv-cpp-python/blob/main/cpp/yolo.cpp#L59
    // It says that each row is a bunch of encoded elements:
    /*
    [0] -> centerX
    [1] -> centerY
    [2] -> width of box in received image
    [3] -> height of box in received image
    [5] -> confidence of the object
    [6-85] -> scores for each class
     */
    private fun getAllObjectsByClass(modelOutput: Array<FloatArray>, importantClassId: Int): List<ClassifiedBox> {
        val result = mutableListOf<ClassifiedBox>()
        for (record in modelOutput) {
            val confidence = record[4]
            if (confidence < CONFIDENCE_THRESHOLD)
                continue
            val maxScoreInd = getIndOfMaxValue(record.takeLast(80)) + 5
            if (record[maxScoreInd] < SCORE_THRESHOLD) continue
            val classId = maxScoreInd - 5
//            if (classId != importantClassId) continue
            result.add(ClassifiedBox(
                record[0] / IMAGE_WIDTH,
                record[1] / IMAGE_HEIGHT,
                record[2] / IMAGE_WIDTH,
                record[3] / IMAGE_HEIGHT,
                classId, confidence))
        }
        return result
    }

    // Rotate the image of the input bitmap
    fun Bitmap.rotate(degrees: Float): Bitmap {
        val matrix = Matrix().apply { postRotate(degrees) }
        return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
    }

    override fun analyze(image: ImageProxy) {
        // Convert the input image to bitmap and resize to 640x640 for model input
        val imgBitmap = image.toBitmap()
        val rawBitmap = imgBitmap?.let { Bitmap.createScaledBitmap(it, 640, 640, false) }
        val bitmap = rawBitmap?.rotate(image.imageInfo.rotationDegrees.toFloat())

        if (bitmap != null) {
            var result = Result()

            val imgData = preProcess(bitmap)
            val inputName = ortSession?.inputNames?.iterator()?.next()
            val shape = longArrayOf(1, 3, 640, 640)
            val env = OrtEnvironment.getEnvironment()
            env.use {
                val tensor = OnnxTensor.createTensor(env, imgData, shape)
                val startTime = SystemClock.uptimeMillis()
                tensor.use {
                    val output = ortSession?.run(Collections.singletonMap(inputName, tensor))
                    output.use {
                        result.processTimeMs = SystemClock.uptimeMillis() - startTime

                        val arr = ((output?.get(0)?.value) as Array<Array<FloatArray>>)[0]

                        val balls = getAllObjectsByClass(arr, 32)

                        val top3 = getTop3(balls)
                        for (ball in top3) {
                            result.detectedScore.clear()
                            result.detectedIndices.clear()
                            result.detectedScore.add(ball.confidence)
                            result.detectedIndices.add(ball.classId)
                        }
                    }
                }
            }
            callBack(result)
        }

        image.close()
    }

    // We can switch analyzer in the app, need to make sure the native resources are freed
    protected fun finalize() {
        ortSession?.close()
    }
}