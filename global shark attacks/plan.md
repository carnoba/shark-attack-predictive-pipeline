# Master Plan - Global Shark Attacks Analysis (Master Level)

## Goal

Execute a high-precision data science pipeline to analyze shark attacks and predict fatality with zero data loss.

## Roadmap

### Phase 1: Data Ingestion & Conversion (Current) - @the-architect

- [x] Initial Directory Discovery
- [x] Create robust ingestion script (`master_pipeline.py`) using `cp1252` encoding.
- [x] Convert `GSAF5.csv` to `master_sharks.db`.
- [x] Verify data integrity (row count check).

### Phase 2: Data Cleaning - @the-janitor

- [x] Standardize 'Date' column and extract 'Month'.
- [x] Clean 'Country' and 'Activity' strings.
- [x] Process 'Fatal' column and create binary `is_fatal` column (1 for Y, 0 for N).
- [x] Execute cleaning and handle missing values.

### Phase 3: Exploratory Data Analysis & Visualization - @the-visionary

- [x] Create visualization script (`visualize_data.py`).
- [x] Generate 'Heatmap of Attacks by Month and Country'.
- [x] Create 'WordCloud of Shark Species'.

### Phase 4: Predictive Modeling - @the-scientist

- [x] Create modeling script (`predict_fatality.py`).
- [x] Build Random Forest Classifier for fatality prediction.
- [x] Evaluate model (Accuracy: 0.7339).

### Phase 5: Deployment - @the-architect

- [x] Design professional Streamlit interface (`app.py`).
- [x] Implement multi-page navigation (Home, Insights, Predictor).
- [ ] Launch and verify application.

---

**Status:** In-Progress (Phase 5)
**Next Step:** Verify the Streamlit app and hand over to the user.
