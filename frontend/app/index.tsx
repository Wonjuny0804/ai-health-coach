import { StyleSheet, Text, View, Pressable } from "react-native";
import { Link } from "expo-router";

export default function Index() {
  return (
    <View style={styles.container}>
      <View style={styles.contentContainer}>
        <View style={styles.headerContainer}>
          <Text style={styles.titleText}>Melian</Text>
          <Text style={styles.subtitleText}>
            An AI partner that will help you reach your health goals
          </Text>
        </View>

        <View style={styles.illustrationContainer}>
          <View style={styles.placeholderIllustration}>
            {/* Placeholder for illustration - will be replaced with actual image */}
            <Text style={styles.placeholderText}>Illustration Placeholder</Text>
          </View>
        </View>

        <Link href={"/sign-in"} asChild>
          <Pressable style={styles.getStartedButton}>
            <Text style={styles.getStartedText}>Get Started</Text>
          </Pressable>
        </Link>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF3D4", // Cream/yellow background color from the image
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
    width: "100%",
  },
  titleText: {
    fontSize: 40,
    fontWeight: "medium",
    textAlign: "center",
    marginBottom: 12,
    fontFamily: "Inter-Medium",
    color: "#1A1A1A",
  },
  subtitleText: {
    fontSize: 18,
    textAlign: "center",
    color: "#333333",
    lineHeight: 24,
    fontFamily: "Inter",
    maxWidth: "90%",
  },
  illustrationContainer: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    marginVertical: 40,
  },
  placeholderIllustration: {
    width: 280,
    height: 280,
    backgroundColor: "#EDDFB3", // Slightly darker than background for visibility
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 2,
    borderColor: "#E5D8AD",
    borderStyle: "dashed",
  },
  placeholderText: {
    color: "#8A7E5C",
    fontSize: 16,
  },
  getStartedButton: {
    backgroundColor: "#E78F37", // Orange color from the image
    paddingVertical: 16,
    borderRadius: 30,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    width: "90%",
  },
  getStartedText: {
    fontSize: 20,
    fontWeight: "500",
    color: "#fff",
    fontFamily: "Inter-Medium",
  },
});
