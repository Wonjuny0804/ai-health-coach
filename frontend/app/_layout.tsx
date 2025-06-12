import { Stack, SplashScreen } from "expo-router";
import { useFonts } from "expo-font";
import { useEffect } from "react";

export default function RootLayout() {
  const [loaded, error] = useFonts({
    "Inter-Regular": require("../assets/fonts/Inter_28pt-Regular.ttf"),
    "Inter-Bold": require("../assets/fonts/Inter_28pt-Bold.ttf"),
    "Inter-SemiBold": require("../assets/fonts/Inter_28pt-SemiBold.ttf"),
    "Inter-Medium": require("../assets/fonts/Inter_28pt-Medium.ttf"),
  })

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error])

  if (!loaded && !error) {
    return null;
  }

  return <Stack screenOptions={{ headerShown: false }} />;
}
