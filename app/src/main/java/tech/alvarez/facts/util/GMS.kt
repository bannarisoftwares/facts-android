package tech.alvarez.facts.util

import com.google.android.gms.common.ConnectionResult
import com.google.android.gms.common.GoogleApiAvailability
import tech.alvarez.facts.App

class GMS {
    companion object {
        fun playStorePackage(): String = GoogleApiAvailability.GOOGLE_PLAY_STORE_PACKAGE
        fun playServicesPackage(): String = GoogleApiAvailability.GOOGLE_PLAY_SERVICES_PACKAGE
        fun playServicesVersionCode(): String =
            GoogleApiAvailability.GOOGLE_PLAY_SERVICES_VERSION_CODE.toString()

        fun isGMSAvailable(): Boolean {
            return GoogleApiAvailability.getInstance()
                .isGooglePlayServicesAvailable(App.applicationContext()) == ConnectionResult.SUCCESS
        }
    }
}