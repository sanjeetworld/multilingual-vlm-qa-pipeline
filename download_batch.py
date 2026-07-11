"""
Batch Image Downloader — Downloads directly into a ZIP file
============================================================
Adapted for: images_scripts_multilingual.jsonl
(fields used: id, image_url — all other fields are just carried
along for reference and are not needed for downloading)

Run this on YOUR PC. Each run downloads the next batch of images
and saves them directly as batch_001.zip, batch_002.zip, etc.

No folder needed. Just run → get zip → upload wherever you need it.

Usage:
  python download_batch.py              # auto: downloads next batch as zip
  python download_batch.py --batch 3    # download a specific batch number
  python download_batch.py --validate 1 # validate & fix corrupt images in batch 1
  python download_batch.py --status     # show overall progress
"""

import json, os, time, argparse, requests, zipfile, io
from datetime import datetime
from PIL import Image

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
# Point this at wherever you keep the jsonl file on your PC.
JSONL_PATH    = r"D:\IIT GN\images_scripts_multilingual.jsonl"
ZIP_DIR       = r"D:\IIT GN\batches"
PROGRESS_FILE = r"D:\IIT GN\download_progress.json"
BATCH_SIZE    = 200      # images per zip
SLEEP_BETWEEN = 0.4      # seconds between requests
TIMEOUT       = 30
RETRY_ATTEMPTS = 3
# ──────────────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": "MultilingualScriptsDatasetProject/1.0 (academic-research; your@email.com)",
}

os.makedirs(ZIP_DIR, exist_ok=True)


# ── Progress tracking ─────────────────────────────────────────────────────────

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed_batches": [], "failed_ids": [], "total_downloaded": 0, "last_updated": None}

def save_progress(progress: dict):
    progress["last_updated"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


# ── Load dataset ──────────────────────────────────────────────────────────────

def load_records() -> list:
    print(f"Loading dataset: {JSONL_PATH}")
    records = []
    skipped = 0
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            # Only id + image_url are required to download; skip anything missing them.
            if not rec.get("id") or not rec.get("image_url"):
                skipped += 1
                continue
            records.append(rec)
    print(f"Total records: {len(records):,}" + (f"  (skipped {skipped:,} malformed/incomplete)" if skipped else ""))
    return records


# ── Download one image into memory ────────────────────────────────────────────

def fetch_image_bytes(img_url: str) -> bytes | None:
    """Download image and return raw bytes (never touches disk)."""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            resp = requests.get(img_url, headers=HEADERS, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            if attempt == RETRY_ATTEMPTS:
                print(f"      ❌ Failed after {RETRY_ATTEMPTS} attempts: {e}")
                return None
            time.sleep(2 ** attempt)
    return None


# ── Validate & fix corrupt images in a zip ────────────────────────────────────

def validate_and_redownload_batch(records: list, batch_num: int, progress: dict):
    """
    Opens every image in the zip, finds corrupt ones,
    re-downloads them, and patches the zip.
    """
    zip_filename = os.path.join(ZIP_DIR, f"batch_{batch_num:03d}.zip")

    if not os.path.exists(zip_filename):
        print(f"❌ {zip_filename} not found. Run download first.")
        return

    print(f"\nValidating {zip_filename} ...")

    corrupt = []
    good    = 0

    # Step 1: Check every image in the zip
    with zipfile.ZipFile(zip_filename, 'r') as zf:
        for name in zf.namelist():
            try:
                data = zf.read(name)
                img  = Image.open(io.BytesIO(data))
                img.verify()
                good += 1
            except Exception:
                corrupt.append(name)
                print(f"  ❌ Corrupt: {name}")

    print(f"\n  ✅ Good    : {good}")
    print(f"  ❌ Corrupt : {len(corrupt)}")

    if not corrupt:
        print("✅ All images are valid! Nothing to fix.")
        return

    # Step 2: Build lookup from id → record
    records_by_id = {r['id']: r for r in records}

    # Step 3: Re-download corrupt images and patch the zip
    print(f"\nRe-downloading {len(corrupt)} corrupt images...")
    fixed     = 0
    still_bad = []

    with zipfile.ZipFile(zip_filename, 'a') as zf:
        for filename in corrupt:
            img_id  = os.path.splitext(filename)[0]

            if img_id not in records_by_id:
                print(f"  ⚠️  ID not in dataset: {img_id}")
                still_bad.append(filename)
                continue

            img_url   = records_by_id[img_id]['image_url']
            img_bytes = fetch_image_bytes(img_url)

            if img_bytes:
                try:
                    img = Image.open(io.BytesIO(img_bytes))
                    img.verify()
                    zf.writestr(filename, img_bytes)
                    print(f"  ✅ Fixed: {img_id}")
                    fixed += 1
                except Exception:
                    print(f"  ❌ Still corrupt after re-download: {img_id}")
                    still_bad.append(filename)
            else:
                still_bad.append(filename)

            time.sleep(SLEEP_BETWEEN)

    print(f"\nRepair complete:")
    print(f"  ✅ Fixed     : {fixed}")
    print(f"  ❌ Still bad : {len(still_bad)}")
    if still_bad:
        print(f"  Still bad   : {[os.path.splitext(f)[0] for f in still_bad]}")
    print(f"  ZIP ready   : {zip_filename}")


# ── Download a batch directly into a ZIP ─────────────────────────────────────

def download_batch_to_zip(records: list, batch_num: int, progress: dict):
    start = (batch_num - 1) * BATCH_SIZE
    end   = min(start + BATCH_SIZE, len(records))
    batch = records[start:end]
    total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE

    zip_filename = os.path.join(ZIP_DIR, f"batch_{batch_num:03d}.zip")
    # Sidecar metadata file: keeps caption/alt_text/category/etc. alongside the images,
    # so the zip is self-describing even without the original jsonl.
    meta_filename = "metadata.jsonl"

    print(f"\n{'='*60}")
    print(f"Batch {batch_num}/{total_batches}  →  images {start}–{end-1}  ({len(batch)} images)")
    print(f"Output ZIP: {zip_filename}")
    print(f"{'='*60}")

    if batch_num in progress["completed_batches"] and os.path.exists(zip_filename):
        print(f"✅ Already done — skipping. Use --validate {batch_num} to check it.")
        return

    success_count = 0
    fail_count    = 0
    meta_lines    = []

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, record in enumerate(batch):
            img_id  = record["id"]
            img_url = record["image_url"]

            ext = img_url.split(".")[-1].split("?")[0].lower()
            if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                ext = "jpg"

            filename_in_zip = f"{img_id}.{ext}"
            img_bytes = fetch_image_bytes(img_url)

            if img_bytes:
                zf.writestr(filename_in_zip, img_bytes)
                success_count += 1
                meta_lines.append(json.dumps(record, ensure_ascii=False))
                print(f"  ✅ [{i+1}/{len(batch)}] {img_id}")
            else:
                fail_count += 1
                if img_id not in progress["failed_ids"]:
                    progress["failed_ids"].append(img_id)
                print(f"  ❌ [{i+1}/{len(batch)}] {img_id}")

            time.sleep(SLEEP_BETWEEN)

        # Bundle metadata (caption, alt_text, category, source, etc.) for the
        # images that actually made it into this zip.
        if meta_lines:
            zf.writestr(meta_filename, "\n".join(meta_lines))

    progress["total_downloaded"] += success_count
    if batch_num not in progress["completed_batches"]:
        progress["completed_batches"].append(batch_num)
    save_progress(progress)

    zip_size_mb = os.path.getsize(zip_filename) / 1e6
    print(f"\nBatch {batch_num} complete:")
    print(f"  ✅ Downloaded : {success_count}")
    print(f"  ❌ Failed     : {fail_count}")
    print(f"  📦 ZIP size   : {zip_size_mb:.1f} MB → {zip_filename}")
    print(f"  Total so far  : {progress['total_downloaded']:,}")


# ── Status summary ────────────────────────────────────────────────────────────

def show_status(records: list, progress: dict):
    total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE
    completed     = len(progress["completed_batches"])
    pct           = (progress["total_downloaded"] / len(records)) * 100 if records else 0

    print(f"\n{'='*60}")
    print(f"DOWNLOAD PROGRESS")
    print(f"{'='*60}")
    print(f"  Total records : {len(records):,}")
    print(f"  Downloaded    : {progress['total_downloaded']:,}  ({pct:.1f}%)")
    print(f"  Failed        : {len(progress['failed_ids']):,}")
    print(f"  Batches done  : {completed}/{total_batches}")
    print(f"  Remaining     : {total_batches - completed} batches")
    if progress["last_updated"]:
        print(f"  Last updated  : {progress['last_updated']}")
    print(f"{'='*60}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch",    type=int, default=None, help="Download specific batch number")
    parser.add_argument("--validate", type=int, default=None, help="Validate & fix a batch zip")
    parser.add_argument("--status",   action="store_true",    help="Show progress summary")
    args = parser.parse_args()

    records  = load_records()
    progress = load_progress()

    if args.status:
        show_status(records, progress)
        return

    if args.validate:
        validate_and_redownload_batch(records, args.validate, progress)
        return

    total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE

    if args.batch:
        if args.batch < 1 or args.batch > total_batches:
            print(f"❌ Batch must be between 1 and {total_batches}.")
            return
        download_batch_to_zip(records, args.batch, progress)
    else:
        completed  = set(progress["completed_batches"])
        next_batch = next((b for b in range(1, total_batches + 1) if b not in completed), None)

        if next_batch is None:
            print("✅ All batches already downloaded!")
            show_status(records, progress)
            return

        print(f"Auto-selected: batch {next_batch}")
        download_batch_to_zip(records, next_batch, progress)

    show_status(records, progress)
    print(f"▶  Run again to get the next batch.")
    print(f"▶  Run --validate {args.batch or 1} to check for corrupt images.")
    print(f"▶  Run --status to see overall progress.")


if __name__ == "__main__":
    main()
