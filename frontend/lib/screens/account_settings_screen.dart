import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'package:image_picker/image_picker.dart';

// import 'dart:convert';
import 'dart:io';

const Media_Base = "http://127.0.0.1:8000";

class AccountSettingsScreen extends StatefulWidget {
  @override
  State<AccountSettingsScreen> createState() => _AccountSettingsScreenState();
}

class _AccountSettingsScreenState extends State<AccountSettingsScreen> {
  Map<String, dynamic>? userData;
  bool loading = true;
  File? _image;

  final ImagePicker _picker = ImagePicker();

  @override
  void initState() {
    super.initState();
    fetchProfile();
  }

  // Fetch user profile data asynchronously
  Future<void> fetchProfile() async {
    final data = await AuthService.getProfile();
    setState(() {
      userData = data;
      loading = false;
    });
  }

  // Function to edit a field and send updated data to the server
  void _editField(String field, String currentValue) {
    TextEditingController controller = TextEditingController(
      text: currentValue,
    );
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Edit $field'),
          content: TextField(
            controller: controller,
            decoration: InputDecoration(labelText: field),
          ),
          actions: [
            TextButton(
              onPressed: () async {
                // Update the value in userData map
                setState(() {
                  userData!['user'][field] = controller.text;
                });

                // Call the PUT request to update user details on the backend
                await _updateUserProfile();

                Navigator.of(context).pop();
              },
              child: Text('Save'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _pickImage() async {
    final picked = await _picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      setState(() {
        _image = File(picked.path);
      });
      if (_image != null) {
        await AuthService.updateProfileImage(_image!);
        // _updateUserProfile(); // Use ! to assert that _image is not null
        fetchProfile();
      }
    }
  }

  // PUT request to update user profile details
  Future<void> _updateUserProfile() async {
    if (userData != null) {
      try {
        await AuthService.updateProfile(userData!); // Pass image separately
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Profile updated successfully")));
      } catch (e) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Failed to update profile: $e")));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Account Settings')),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : userData == null
              ? const Center(child: Text('Failed to load profile'))
              : Padding(
                padding: const EdgeInsets.all(16),
                child: ListView(
                  children: [
                    if (userData!['profile_image_url'] != null)
                      Center(
                        child: CircleAvatar(
                          radius: 50,
                          backgroundImage: NetworkImage(
                            Media_Base + userData!['profile_image_url'],
                          ),
                        ),
                      ),
                    const SizedBox(height: 20),
                    TextButton(
                      onPressed: _pickImage,
                      child: Text('Pick a new profile image'),
                    ),
                    const SizedBox(height: 20),

                    // Editable fields
                    _buildEditableField(
                      'Username',
                      userData!['user']['username'],
                      () =>
                          _editField('username', userData!['user']['username']),
                    ),
                    _buildEditableField(
                      'Email',
                      userData!['user']['email'],
                      () => _editField('email', userData!['user']['email']),
                    ),
                    _buildEditableField(
                      'First Name',
                      userData!['user']['first_name'],
                      () => _editField(
                        'first_name',
                        userData!['user']['first_name'],
                      ),
                    ),
                    _buildEditableField(
                      'Last Name',
                      userData!['user']['last_name'],
                      () => _editField(
                        'last_name',
                        userData!['user']['last_name'],
                      ),
                    ),
                  ],
                ),
              ),
    );
  }

  // Helper method to build each editable field row
  Widget _buildEditableField(
    String label,
    String currentValue,
    VoidCallback onTap,
  ) {
    return ListTile(
      title: Text(label),
      subtitle: Text(currentValue),
      trailing: Icon(Icons.edit),
      onTap: onTap,
    );
  }
}
