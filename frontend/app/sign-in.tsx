import { StyleSheet, Text, View, Pressable } from "react-native";
import { router } from "expo-router";

export default function SignIn() {
  return (
    <View style={styles.container}>
      <View style={styles.contentContainer}>
        <View style={styles.headerContainer}>
          <Text style={styles.titleText}>Sign In</Text>
          <Text style={styles.subtitleText}>
            Choose how you want to continue
          </Text>
        </View>
        
        <View style={styles.buttonContainer}>
          {/* Email Sign In Button */}
          <Pressable 
            style={[styles.signInButton, styles.emailButton]}
            onPress={() => console.log("Email Sign In pressed")}
          >
            <Text style={styles.emailButtonText}>Continue with Email</Text>
          </Pressable>
        </View>
        
        <Pressable onPress={() => router.back()}>
          <Text style={styles.backButton}>Back to Home</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF3D4", // Matching landing page background color
  },
  contentContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "space-between",
    paddingTop: 80,
    paddingBottom: 60,
    paddingHorizontal: 24,
  },
  headerContainer: {
    alignItems: "center",
    marginBottom: 40,
    width: "100%",
  },
  titleText: {
    fontSize: 36,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 12,
    fontFamily: "Inter-Bold",
    color: "#1A1A1A",
  },
  subtitleText: {
    fontSize: 18,
    textAlign: "center",
    color: "#333333",
    lineHeight: 24,
    fontFamily: "Inter",
  },
  buttonContainer: {
    width: "100%",
    gap: 16,
  },
  signInButton: {
    paddingVertical: 16,
    borderRadius: 30,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    width: "100%",
  },
  googleButton: {
    backgroundColor: "#ffffff",
    borderWidth: 1,
    borderColor: "#dddddd",
  },
  googleButtonText: {
    fontSize: 18,
    fontWeight: "500",
    color: "#000000",
    fontFamily: "Inter-Medium",
  },
  appleButton: {
    backgroundColor: "#000000",
  },
  appleButtonText: {
    fontSize: 18,
    fontWeight: "500",
    color: "#ffffff",
    fontFamily: "Inter-Medium",
  },
  emailButton: {
    backgroundColor: "#E78F37", // Orange button matching landing page
    borderWidth: 0,
  },
  emailButtonText: {
    fontSize: 18,
    fontWeight: "500",
    color: "#ffffff",
    fontFamily: "Inter-Medium",
  },
  backButton: {
    fontSize: 16,
    color: "#333333",
    marginTop: 20,
    textDecorationLine: "underline",
    fontFamily: "Inter",
  },
});
