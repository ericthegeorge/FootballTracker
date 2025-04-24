import 'dart:convert';
// import 'dart:developer';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // testing url

  static Future<http.Response> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login/'),
      body: {'username': username, 'password': password},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      await prefs.setBool('is_staff', data['is_staff']);
      await prefs.setString('username', data['username']);
    }

    return response;
  }

  static Future<http.Response> register(
    String username,
    String email,
    String password,
    String firstname,
    String lastname, [
    File? image, //optional
    bool isAdmin = false,
  ]) async {
    var uri = Uri.parse('$baseUrl/register/');
    var request = http.MultipartRequest('POST', uri);

    request.fields['username'] = username;
    request.fields['email'] = email;
    request.fields['password'] = password;
    request.fields['first_name'] = firstname;
    request.fields['last_name'] = lastname;
    request.fields['is_staff'] = isAdmin.toString();

    print(request);

    if (image != null) {
      request.files.add(
        await http.MultipartFile.fromPath('picture', image.path),
      );
    }

    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    var code = response.statusCode;
    if (code == 200 || code == 201) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', data['token']);
      // print(data['is_staff']);
      await prefs.setBool('is_staff', data['is_staff']);
      await prefs.setString('username', data['username']);
    }

    return response;
  }

  static Future<String?> getUsername() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('username');
  }

  static Future<bool> isAdmin() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('is_staff') ?? false;
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('token');
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  static Future<Map<String, dynamic>?> getProfile() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final username = prefs.getString(
      'username',
    ); // <-- make sure you're storing this at login/signup

    final response = await http.get(
      Uri.parse(
        '$baseUrl/user-profile/?username=$username',
      ), // <-- query parameter
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      // print(jsonDecode(response.body));
      return jsonDecode(response.body);
    } else {
      print("Failed to fetch profile: ${response.body}");
      return null;
    }
  }

  static Future<void> updateProfile(Map<String, dynamic> userData) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final oldUsername = prefs.getString('username');

    var uri = Uri.parse('$baseUrl/user/?username=$oldUsername');

    print(userData['user']);

    var response = await http.put(
      uri,
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'username': userData['user']['username'],
        'email': userData['user']['email'],
        'first_name': userData['user']['first_name'],
        'last_name': userData['user']['last_name'],
      }),
    );

    if (response.statusCode == 200) {
      await prefs.setString('username', userData['user']['username']);
      await prefs.setString('email', userData['user']['email']);
      await prefs.setString('first_name', userData['user']['first_name']);
      await prefs.setString('last_name', userData['user']['last_name']);
    } else {
      throw "Failed to update profile";
    }
  }

  static Future<void> updateProfileImage(File image) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final prefsusername = prefs.getString('username');

    var uri = Uri.parse('$baseUrl/user-profile/?username=$prefsusername');
    var request = http.MultipartRequest('PUT', uri);
    request.headers['Authorization'] = 'Token $token';

    // Add the profile image to the request
    request.files.add(
      await http.MultipartFile.fromPath('profile_image', image.path),
    );

    // Send the request
    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    // Log the response body for debugging
    print("Response Body: ${response.body}");

    // Check response status and handle success or failure
    if (response.statusCode == 200) {
      // Optionally, update the shared preferences or other state if needed
      print("Profile image updated successfully.");
    } else {
      // Handle the error
      throw "Failed to update profile image. Error: ${response.body}";
    }
  }
}
