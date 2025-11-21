# Creativity Rating App - Streamlit Version

A web-based application for collecting subjective ratings of soccer actions from video clips. This is a Streamlit port of the original Kivy desktop application, designed to be deployable as a web app.

## Features

- **Multi-page navigation**: Welcome → Login → Questionnaire → Video Rating
- **Dynamic form generation**: Questionnaire and rating scales are fully configurable via YAML files
- **User ID system**: Anonymous user identification based on demographic data
- **Video playback**: Stream videos with optional metadata and pitch visualization
- **Data persistence**: Automatic saving of user data and ratings to JSON files
- **CSV export**: Export all data to CSV format with statistics

## Installation

1. **Clone or navigate to this directory**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Edit `config/config.yaml` to set paths to your database and videos
   - Edit `config/questionnaire_fields.yaml` to customize the questionnaire
   - Edit `config/rating_scales.yaml` to customize rating scales

## Running the Application

### Local Development

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Production Deployment

For deploying to Streamlit Cloud or other hosting platforms:

1. **Streamlit Cloud**:
   - Push this repository to GitHub
   - Connect your GitHub repo to Streamlit Cloud
   - Set the main file path to `app.py`
   - Configure secrets and environment variables as needed

2. **Other platforms** (Docker, Heroku, etc.):
   - Ensure `requirements.txt` is properly configured
   - Set up environment variables for paths
   - Use `streamlit run app.py` as the startup command

## Configuration

### Main Configuration (`config/config.yaml`)

```yaml
paths:
  metadata_path: "/path/to/metadata.duckdb"  # DuckDB database or CSV file with event metadata
  video_path: "/path/to/videos/"             # Directory containing .mp4 files

settings:
  min_ratings_per_video: 2  # Stop showing videos after N ratings collected
  questionnaire_fields_file: "config/questionnaire_fields.yaml"
  rating_scales_file: "config/rating_scales.yaml"
  display_metadata: true  # Show metadata (team, player, type, etc.)
  display_pitch: true  # Show pitch visualization
  video_playback_mode: "loop"  # "loop" or "once"
    # - "loop": Video autoplays, repeats automatically, controls visible
    # - "once": Video autoplays once, no controls, cannot be replayed
```

### Questionnaire Fields (`config/questionnaire_fields.yaml`)

Define demographic and experience fields:
- `type`: "multiple_choice", "text", or "numeric"
- `active`: true/false to enable/disable fields
- `required_to_proceed`: true/false for mandatory fields

### Rating Scales (`config/rating_scales.yaml`)

Define rating dimensions:
- `type`: "discrete", "slider", or "text"
- `active`: true/false to enable/disable scales
- `required_to_proceed`: true/false for mandatory scales

## Directory Structure

```
streamlit-creativity-app/
├── app.py                    # Main application file
├── pages/                    # Page modules
│   ├── welcome.py           # Welcome screen
│   ├── login.py             # Login/returning user screen
│   ├── questionnaire.py     # Demographic questionnaire
│   └── videoplayer.py       # Video rating interface
├── utils/                    # Utility modules
│   ├── user.py              # User class
│   ├── config_loader.py     # Configuration loading
│   ├── data_persistence.py  # Data saving/loading
│   └── export_to_csv.py     # CSV export functionality
├── config/                   # Configuration files
│   ├── config.yaml
│   ├── questionnaire_fields.yaml
│   └── rating_scales.yaml
├── user_data/               # Saved user demographics (JSON)
├── user_ratings/            # Saved ratings (JSON)
├── output/                  # CSV exports
├── backup/                  # Auto-backup of JSON files
└── requirements.txt         # Python dependencies
```

## Key Differences from Kivy Version

### Advantages
- **Web-based**: No installation required for users
- **Cross-platform**: Works on any device with a browser
- **Easier deployment**: Can be hosted on cloud platforms
- **Simpler code**: Streamlit handles UI rendering automatically

### Limitations
- **No offline mode**: Requires internet connection (unless self-hosted)
- **Session-based**: Users must complete in one session or remember their User ID
- **Less keyboard control**: Mouse/touch interaction only

## Data Management

### Saving Data

- **User data**: Saved to `user_data/{user_id}.json` after questionnaire
- **Ratings**: Saved to `user_ratings/{user_id}_{action_id}.json` after each video

### Exporting Data

Run the export script manually:
```bash
python utils/export_to_csv.py
```

Or use the "Export Data" button in the app when all videos are rated.

Exports create:
- `output/ratings.csv` - All individual ratings
- `output/mean_ratings.csv` - Aggregated statistics per action
- `output/users.csv` - All user demographics
- `output/rating_log.txt` - Summary statistics
- `backup/` - Copies of all JSON files

## Customization

### Adding New Questionnaire Fields

Edit `config/questionnaire_fields.yaml`:

```yaml
- active: true
  type: "multiple_choice"  # or "text" or "numeric"
  field_name: "new_field"
  title: "Question text"
  options: ["Option 1", "Option 2"]  # for multiple_choice only
```

### Adding New Rating Scales

Edit `config/rating_scales.yaml`:

```yaml
- active: true
  type: "discrete"  # or "slider" or "text"
  title: "New Scale"
  label_low: "low end label"
  label_high: "high end label"
  values: [1, 2, 3, 4, 5]  # for discrete only
  required_to_proceed: true
```

## Troubleshooting

### Videos not loading
- Check that `video_path` in `config.yaml` is correct
- Ensure video files are .mp4 format
- Verify file permissions

### Metadata loading errors
- Check that `metadata_path` in `config.yaml` points to valid DuckDB (.duckdb) or CSV (.csv) file
- For DuckDB: Ensure database has `events` table with required columns
- For CSV: Ensure file has an `id` column matching video filenames (without .mp4)

### Configuration errors
- Validate YAML syntax using an online validator
- Ensure all required fields are present in config files

## Credits

Adapted from the Kivy-based Creativity Rating App for desktop environments.

## License

[Your license here]
