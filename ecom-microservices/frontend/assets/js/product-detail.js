// 1. Configuration
const CONFIG = {
  API: {
      BASE_URL: 'http://localhost:8005',
      CART_URL: 'http://localhost:8003'
  },
  ASSETS: {
      DEFAULT_IMAGE: '/assets/images/product-default.png'
  },
  UI: {
      STATUS_BADGES: {
          ACTIVE: 'bg-success',
          INACTIVE: 'bg-danger',
          OUT_OF_STOCK: 'bg-warning'
      },
      FORMATS: {
          BOOK: {
              PAPERBACK: 'Bìa mềm',
              HARDCOVER: 'Bìa cứng',
              EBOOK: 'Sách điện tử',
              AUDIOBOOK: 'Sách nói'
          }
      }
  },
  DATE_FORMAT: {
      FULL: {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
      },
      SHORT: {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
      }
  }
};

// 2. Utility Functions
const Utils = {
  formatters: {
      price(price) {
          if (!price) return '0';
          return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
      },

      date(dateString, format = 'SHORT') {
          if (!dateString) return 'Chưa có thông tin';
          return new Date(dateString).toLocaleString('vi-VN', CONFIG.DATE_FORMAT[format]);
      }
  },

  calculators: {
      discount(salePrice, basePrice) {
          if (!salePrice || !basePrice) return 0;
          if (parseFloat(salePrice) >= parseFloat(basePrice)) return 0;
          const discount = Math.round((1 - parseFloat(salePrice) / parseFloat(basePrice)) * 100);
          return Math.min(Math.max(discount, 0), 100);
      }
  },

  dom: {
      createRatingStars(rating) {
          const stars = Math.round(rating || 0);
          return Array(5).fill('').map((_, i) => 
              `<i class="fas fa-star ${i < stars ? 'text-warning' : 'text-muted'}"></i>`
          ).join('');
      }
  },

  parsers: {
      authors(authors) {
          if (Array.isArray(authors)) return authors.join(', ');
          if (typeof authors === 'string') return authors.replace(/[\[\]']/g, '');
          return 'Không rõ';
      },

      tableOfContents(contents) {
          if (!contents) return [];
          if (typeof contents === 'string') {
              try {
                  return JSON.parse(contents.replace(/'/g, '"'));
              } catch {
                  return contents.replace(/[\[\]']/g, '').split(',');
              }
          }
          return contents;
      }
  }
};

// 3. Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  initializeProductPage();
});

// 4. Core Functions
function initializeProductPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const productId = urlParams.get('id');
  
  if (!productId) {
      showError('Không tìm thấy sản phẩm!');
      return;
  }
  
  fetchProductDetail(productId);
}

async function fetchProductDetail(productId) {
  try {
      const response = await fetch(`${CONFIG.API.BASE_URL}/products/${productId}`);
      if (!response.ok) throw new Error('Không thể tải chi tiết sản phẩm');
      
      const product = await response.json();
      renderProductDetail(product);
  } catch (error) {
      console.error('Error:', error);
      showError(error.message);
  }
}

function showError(message) {
  const container = document.getElementById('productDetail');
  container.innerHTML = `
      <div class="alert alert-danger">
          <i class="fas fa-exclamation-circle me-2"></i>${message}
      </div>
  `;
}

// 5. Render Functions
function renderProductDetail(product) {
  const container = document.getElementById('productDetail');
  const discountPercentage = Utils.calculators.discount(product.sale_price, product.base_price);
  const additionalImages = product.image_urls || [];

  const productDetailHTML = `
      <div class="container-fluid px-4 py-5 product-detail-container">
          <div class="row g-4">
              ${renderImageGallery(product, discountPercentage, additionalImages)}
              ${renderProductInfo(product)}
          </div>
          ${renderProductTabs(product)}
      </div>
  `;

  container.innerHTML = productDetailHTML;
  setupProductInteractions(product);
}

function renderImageGallery(product, discountPercentage, additionalImages) {
  return `
      <div class="col-lg-6 col-md-12">
          <div class="product-gallery card shadow-sm p-3">
              <!-- Main Image Container -->
              <div class="main-image-container mb-3">
                  <div class="position-relative">
                      <img 
                          src="${product.primary_image || CONFIG.ASSETS.DEFAULT_IMAGE}" 
                          class="main-product-image img-fluid rounded w-100"
                          alt="${product.name}"
                          onerror="this.onerror=null;this.src='${CONFIG.ASSETS.DEFAULT_IMAGE}';"
                      >
                      <!-- Badges -->
                      ${discountPercentage > 0 ? `
                          <div class="position-absolute top-0 start-0 m-3">
                              <span class="badge bg-danger px-3 py-2">
                                  -${discountPercentage}% GIẢM
                              </span>
                          </div>
                      ` : ''}
                      ${product.status !== 'ACTIVE' ? `
                          <div class="position-absolute top-0 end-0 m-3">
                              <span class="badge ${CONFIG.UI.STATUS_BADGES[product.status]} px-3 py-2">
                                  ${product.status}
                              </span>
                          </div>
                      ` : ''}
                      <!-- Zoom Icon -->
                      <div class="position-absolute bottom-0 end-0 m-3">
                          <button class="btn btn-light btn-sm" onclick="ImageGallery.openLightbox('${product.primary_image}')">
                              <i class="fas fa-search-plus"></i>
                          </button>
                      </div>
                  </div>
              </div>

              <!-- Thumbnails -->
              ${additionalImages?.length ? `
                  <div class="thumbnails-container">
                      <div class="d-flex flex-wrap gap-2 justify-content-center">
                          <div class="thumbnail-item active" onclick="updateMainImage(this, '${product.primary_image}')">
                              <img 
                                  src="${product.primary_image}" 
                                  class="thumbnail-image rounded border"
                                  alt="Main view"
                              >
                          </div>
                          ${additionalImages.map(img => `
                              <div class="thumbnail-item" onclick="updateMainImage(this, '${img}')">
                                  <img 
                                      src="${img}" 
                                      class="thumbnail-image rounded border"
                                      alt="Product view"
                                  >
                              </div>
                          `).join('')}
                      </div>
                  </div>
              ` : ''}
          </div>
      </div>
  `;
}

// Thêm function để cập nhật ảnh chính
function updateMainImage(thumbnailElement, imageSrc) {
  // Remove active class from all thumbnails
  document.querySelectorAll('.thumbnail-item').forEach(item => {
      item.classList.remove('active');
  });

  // Add active class to clicked thumbnail
  thumbnailElement.classList.add('active');

  // Update main image
  const mainImage = document.querySelector('.main-product-image');
  mainImage.src = imageSrc;
}

function renderThumbnails(additionalImages) {
  if (!additionalImages?.length) return '';
  
  return `
      <div class="thumbnail-gallery mt-3 px-2">
          <div class="d-flex flex-wrap gap-2 justify-content-center">
              ${additionalImages.map(img => `
                  <div class="thumbnail-wrapper" onclick="updateMainImage(this)">
                      <img 
                          src="${img}" 
                          class="thumbnail-image rounded border"
                          data-full="${img}"
                          alt="Product view"
                          onerror="this.onerror=null;this.src='${CONFIG.ASSETS.DEFAULT_IMAGE}';"
                      >
                  </div>
              `).join('')}
          </div>
      </div>
  `;
}

// 7. Product Info Functions
function renderProductInfo(product) {
  return `
      <div class="col-lg-6 col-md-12">
          <div class="product-info-container">
              ${renderHeader(product)}
              ${renderRatingSection(product)}
              ${renderPriceSection(product)}
              ${renderStockInfo(product)}
              ${renderSpecifications(product)}
              ${renderPurchaseActions(product)}
          </div>
      </div>
  `;
}

function renderHeader(product) {
  return `
      <div class="product-header mb-4">
          <div class="d-flex justify-content-between align-items-start">
              <h1 class="product-title fw-bold mb-2">${product.name}</h1>
              <button class="btn btn-outline-primary wishlist-btn" onclick="toggleWishlist('${product._id}')">
                  <i class="far fa-heart"></i>
              </button>
          </div>
          <div class="product-meta d-flex flex-wrap gap-3 text-muted">
              <span class="sku">
                  <i class="fas fa-barcode me-1"></i> ${product.sku}
              </span>
              <span class="brand">
                  <i class="fas fa-tag me-1"></i> ${product.brand || 'Không có'}
              </span>
              <span class="category">
                  <i class="fas fa-folder me-1"></i> ${product.category_path.join(' > ')}
              </span>
          </div>
      </div>
  `;
}

function renderRatingSection(product) {
  return `
      <div class="rating-section card bg-light p-3 mb-4">
          <div class="d-flex justify-content-between align-items-center">
              <div class="rating-stars">
                  ${Utils.dom.createRatingStars(product.rating)}
                  <span class="ms-2 text-muted">(${product.review_count || 0} đánh giá)</span>
              </div>
              <div class="product-stats">
                  <span class="me-3">
                      <i class="fas fa-eye text-primary"></i> ${product.total_views || 0}
                  </span>
                  <span>
                      <i class="fas fa-shopping-cart text-success"></i> ${product.total_sold || 0}
                  </span>
              </div>
          </div>
      </div>
  `;
}

function renderPriceSection(product) {
  return `
      <div class="price-section card p-3 mb-4">
          <div class="d-flex align-items-center">
              <div class="current-price">
                  <span class="h2 text-primary mb-0">
                      ${Utils.formatters.price(product.current_price)}₫
                  </span>
                  ${product.sale_price ? `
                      <span class="original-price ms-2 text-muted text-decoration-line-through">
                          ${Utils.formatters.price(product.base_price)}₫
                      </span>
                  ` : ''}
              </div>
          </div>
      </div>
  `;
}

function renderStockInfo(product) {
  const isLowStock = product.quantity <= product.low_stock_threshold;
  const stockPercentage = Math.min((product.quantity / 100) * 100, 100);
  
  return `
      <div class="stock-info card p-3 mb-4">
          <div class="d-flex justify-content-between align-items-center mb-2">
              <span>
                  <i class="fas fa-box-open me-2"></i>Tình trạng kho
              </span>
              <span class="${isLowStock ? 'text-warning' : 'text-success'}">
                  ${product.quantity} sản phẩm có sẵn
              </span>
          </div>
          <div class="progress" style="height: 5px;">
              <div class="progress-bar ${isLowStock ? 'bg-warning' : 'bg-success'}" 
                   role="progressbar" 
                   style="width: ${stockPercentage}%">
              </div>
          </div>
          ${isLowStock ? `
              <div class="text-warning small mt-2">
                  <i class="fas fa-exclamation-triangle me-1"></i>
                  Sắp hết hàng
              </div>
          ` : ''}
      </div>
  `;
}
function renderSpecifications(product) {
  return `
      <div class="specifications-section card p-3 mb-4">
          <h6 class="card-title mb-3">
              <i class="fas fa-clipboard-list me-2"></i>Thông số chi tiết
          </h6>
          <div class="specs-grid">
              <div class="row g-3">
                  <div class="col-6">
                      <small class="text-muted d-block">Kích thước</small>
                      <span>${product.dimensions.length} x ${product.dimensions.width} x ${product.dimensions.height} cm</span>
                  </div>
                  <div class="col-6">
                      <small class="text-muted d-block">Khối lượng</small>
                      <span>${product.weight} kg</span>
                  </div>
                  ${product.product_type === 'BOOK' ? `
                      <div class="col-6">
                          <small class="text-muted d-block">Định dạng</small>
                          <span>${CONFIG.UI.FORMATS.BOOK[product.details?.format] || 'Không có'}</span>
                      </div>
                      <div class="col-6">
                          <small class="text-muted d-block">Số trang</small>
                          <span>${product.details?.page_count || 'Không có'}</span>
                      </div>
                  ` : ''}
              </div>
          </div>
      </div>
  `;
}

function renderPurchaseActions(product) {
  return `
      <div class="purchase-section card p-4">
          <div class="quantity-selector mb-3">
              <label class="form-label">Số lượng:</label>
              <div class="input-group">
                  <button class="btn btn-outline-secondary" type="button" id="minus-btn">
                      <i class="fas fa-minus"></i>
                  </button>
                  <input type="number" 
                         class="form-control text-center" 
                         id="quantity-input"
                         value="1"
                         min="1"
                         max="${product.quantity}"
                         ${product.quantity === 0 ? 'disabled' : ''}
                  >
                  <button class="btn btn-outline-secondary" type="button" id="plus-btn">
                      <i class="fas fa-plus"></i>
                  </button>
              </div>
          </div>

          <div class="d-grid gap-2">
              <button class="btn btn-primary btn-lg add-to-cart" 
                      ${product.quantity === 0 ? 'disabled' : ''}>
                  <i class="fas fa-shopping-cart me-2"></i>
                  Thêm vào giỏ hàng
              </button>
              <button class="btn btn-outline-primary btn-lg buy-now"
                      ${product.quantity === 0 ? 'disabled' : ''}>
                  <i class="fas fa-bolt me-2"></i>
                  Mua ngay
              </button>
          </div>

          ${product.quantity === 0 ? `
              <div class="alert alert-warning mt-3 mb-0">
                  <i class="fas fa-exclamation-circle me-2"></i>
                  Sản phẩm hiện đang hết hàng
              </div>
          ` : ''}
      </div>
  `;
}

// 8. Product Tabs Functions
function renderProductTabs(product) {
  return `
      <div class="product-tabs mt-5">
          <div class="card shadow-sm">
              <div class="card-body">
                  <nav>
                      <div class="nav nav-tabs nav-fill" id="product-tabs" role="tablist">
                          <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#details">
                              <i class="fas fa-list me-2"></i>Thông tin chi tiết
                          </button>
                          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#reviews">
                              <i class="fas fa-star me-2"></i>Đánh giá (${product.review_count || 0})
                          </button>
                      </div>
                  </nav>

                  <div class="tab-content py-4">
                      <div class="tab-pane fade show active" id="details">
                          ${renderProductDetails(product)}
                      </div>
                      <div class="tab-pane fade" id="reviews">
                          ${renderReviewsTab(product)}
                      </div>
                  </div>
              </div>
          </div>
      </div>
  `;
}

function renderProductDescription(product) {
  return `
      <div class="product-description">
          ${product.description ? `
              <div class="description-content">
                  ${product.description}
              </div>
          ` : `
              <div class="text-center text-muted py-5">
                  <i class="fas fa-file-alt fa-3x mb-3"></i>
                  <p>Chưa có mô tả cho sản phẩm này</p>
              </div>
          `}
      </div>
  `;
}
function renderProductDetails(product) {
  // Render common specifications first
  const commonSpecs = `
      <div class="common-specifications mb-4">
          <h5 class="mb-3">Thông số cơ bản</h5>
          <div class="row g-3">
              <div class="col-6">
                  <small class="text-muted d-block">Mã sản phẩm</small>
                  <span>${product.sku}</span>
              </div>
              <div class="col-6">
                  <small class="text-muted d-block">Thương hiệu</small>
                  <span>${product.brand}</span>
              </div>
              <div class="col-6">
                  <small class="text-muted d-block">Kích thước</small>
                  <span>${product.dimensions.length} x ${product.dimensions.width} x ${product.dimensions.height} cm</span>
              </div>
              <div class="col-6">
                  <small class="text-muted d-block">Khối lượng</small>
                  <span>${product.weight} kg</span>
              </div>
          </div>
      </div>
  `;

  // Then render type-specific details
  let specificDetails = '';
  switch (product.product_type) {
      case 'BOOK':
          specificDetails = renderBookDetails(product.details);
          break;
      case 'SHOE':
          specificDetails = renderShoeDetails(product.details);
          break;
      default:
          specificDetails = renderDefaultDetails(product);
  }

  return `
      <div class="product-details">
          ${commonSpecs}
          ${specificDetails}
      </div>
  `;
}

function renderBookDetails(details) {
  // Book-specific fields
  return `
      <div class="book-specific-details">
          <div class="row g-4">
              <div class="col-md-6">
                  <div class="card h-100">
                      <div class="card-body">
                          <h5 class="card-title mb-4">
                              <i class="fas fa-book me-2"></i>Thông tin sách
                          </h5>
                          <ul class="list-group list-group-flush">
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">ISBN-13</span>
                                  <span class="fw-medium">${details.isbn_13}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Số trang</span>
                                  <span class="fw-medium">${details.page_count}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Phiên bản</span>
                                  <span class="fw-medium">${details.edition}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Ngày xuất bản</span>
                                  <span class="fw-medium">${Utils.formatters.date(details.publication_date)}</span>
                              </li>
                          </ul>
                      </div>
                  </div>
              </div>
              <div class="col-md-6">
                  <div class="card h-100">
                      <div class="card-body">
                          <h5 class="card-title mb-4">
                              <i class="fas fa-info-circle me-2"></i>Chi tiết
                          </h5>
                          <ul class="list-group list-group-flush">
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Series</span>
                                  <span class="fw-medium">${details.series || 'Không có'}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Tập</span>
                                  <span class="fw-medium">${details.volume || 'Không có'}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Định dạng</span>
                                  <span class="fw-medium">${details.book_format}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Độ tuổi</span>
                                  <span class="fw-medium">${details.reading_age}</span>
                              </li>
                          </ul>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  `;
}

function renderShoeDetails(details) {
  // Shoe-specific fields
  return `
      <div class="shoe-specific-details">
          <div class="row g-4">
              <div class="col-md-6">
                  <div class="card h-100">
                      <div class="card-body">
                          <h5 class="card-title mb-4">
                              <i class="fas fa-shoe-prints me-2"></i>Thông tin giày
                          </h5>
                          <ul class="list-group list-group-flush">
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Size</span>
                                  <span class="fw-medium">${details.size}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Màu sắc</span>
                                  <span class="fw-medium">${details.color}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Chất liệu</span>
                                  <span class="fw-medium">${details.material}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Giới tính</span>
                                  <span class="fw-medium">${details.gender === 'M' ? 'Nam' : 'Nữ'}</span>
                              </li>
                          </ul>
                      </div>
                  </div>
              </div>
              <div class="col-md-6">
                  <div class="card h-100">
                      <div class="card-body">
                          <h5 class="card-title mb-4">
                              <i class="fas fa-cog me-2"></i>Thông số kỹ thuật
                          </h5>
                          <ul class="list-group list-group-flush">
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Loại thể thao</span>
                                  <span class="fw-medium">${details.sport_type}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Kiểu dáng</span>
                                  <span class="fw-medium">${details.style}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Chất liệu đế</span>
                                  <span class="fw-medium">${details.sole_material}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Chất liệu upper</span>
                                  <span class="fw-medium">${details.upper_material}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Độ thoáng khí</span>
                                  <span class="fw-medium">${details.breathability}</span>
                              </li>
                              <li class="list-group-item d-flex justify-content-between">
                                  <span class="text-muted">Địa hình phù hợp</span>
                                  <span class="fw-medium">${details.recommended_terrain}</span>
                              </li>
                          </ul>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  `;
}
function renderTableOfContents(contents) {
  const parsedContents = Utils.parsers.tableOfContents(contents);
  if (!parsedContents.length) return '';

  return `
      <div class="list-group list-group-flush">
          ${parsedContents.map((item, index) => `
              <div class="list-group-item">
                  <span class="chapter-number text-primary me-2">${index + 1}.</span>
                  <span class="chapter-title">${item}</span>
              </div>
          `).join('')}
      </div>
  `;
}

// 9. Reviews Functions
function renderReviewsTab(product) {
  return `
      <div class="reviews-container">
          ${renderReviewsSummary(product)}
          ${renderReviewsList(product.reviews)}
          ${renderReviewForm(product._id)}
      </div>
  `;
}

function renderReviewsSummary(product) {
  const avgRating = product.rating || 0;
  const totalReviews = product.review_count || 0;
  
  return `
      <div class="reviews-summary card mb-4">
          <div class="card-body">
              <div class="row align-items-center">
                  <div class="col-md-4 text-center border-end">
                      <div class="h1 mb-0">${avgRating.toFixed(1)}</div>
                      <div class="rating-stars fs-4 my-2">
                          ${Utils.dom.createRatingStars(avgRating)}
                      </div>
                      <div class="text-muted">
                          ${totalReviews} ${totalReviews === 1 ? 'đánh giá' : 'đánh giá'}
                      </div>
                  </div>
                  <div class="col-md-8 ps-4">
                      ${renderRatingDistribution(product.rating_distribution)}
                  </div>
              </div>
          </div>
      </div>
  `;
}

function renderRatingDistribution(distribution = {}) {
  const total = Object.values(distribution).reduce((a, b) => a + b, 0);
  const stars = [5, 4, 3, 2, 1];
  
  return `
      <div class="rating-distribution">
          ${stars.map(star => {
              const count = distribution[star] || 0;
              const percentage = total ? (count / total) * 100 : 0;
              
              return `
                  <div class="rating-bar d-flex align-items-center mb-2">
                      <div class="rating-label me-2" style="min-width: 60px">
                          ${star} <i class="fas fa-star text-warning"></i>
                      </div>
                      <div class="progress flex-grow-1" style="height: 8px">
                          <div class="progress-bar bg-warning" 
                               role="progressbar" 
                               style="width: ${percentage}%" 
                               aria-valuenow="${percentage}" 
                               aria-valuemin="0" 
                               aria-valuemax="100">
                          </div>
                      </div>
                      <div class="rating-count ms-2" style="min-width: 40px">
                          ${count}
                      </div>
                  </div>
              `;
          }).join('')}
      </div>
  `;
}

function renderReviewsList(reviews = []) {
  if (!reviews.length) {
      return `
          <div class="text-center py-5">
              <i class="far fa-comment-alt fa-3x text-muted mb-3"></i>
              <p class="lead mb-0">Chưa có đánh giá nào</p>
              <p class="text-muted">Hãy là người đầu tiên đánh giá sản phẩm này</p>
          </div>
      `;
  }

  return `
      <div class="reviews-list">
          ${reviews.map(review => `
              <div class="review-item card mb-3">
                  <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                          <div class="reviewer-info">
                              <h6 class="mb-1">${review.user_name}</h6>
                              <div class="rating-stars mb-1">
                                  ${Utils.dom.createRatingStars(review.rating)}
                              </div>
                              <small class="text-muted">
                                  <i class="far fa-clock me-1"></i>
                                  ${Utils.formatters.date(review.created_at)}
                              </small>
                          </div>
                          ${review.verified_purchase ? `
                              <div class="verified-badge">
                                  <span class="badge bg-success">
                                      <i class="fas fa-check-circle me-1"></i>Đã mua hàng
                                  </span>
                              </div>
                          ` : ''}
                      </div>
                      <div class="review-content">
                          ${review.title ? `<h6 class="review-title mb-2">${review.title}</h6>` : ''}
                          <p class="mb-0">${review.comment}</p>
                      </div>
                      ${review.images?.length ? `
                          <div class="review-images mt-3">
                              <div class="d-flex gap-2">
                                  ${review.images.map(img => `
                                      <img src="${img}" 
                                           class="review-image rounded" 
                                           alt="Review image"
                                           style="width: 80px; height: 80px; object-fit: cover;"
                                           onclick="showImageModal('${img}')"
                                      >
                                  `).join('')}
                              </div>
                          </div>
                      ` : ''}
                  </div>
              </div>
          `).join('')}
      </div>
  `;
}

function renderReviewForm(productId) {
  const isLoggedIn = !!localStorage.getItem('accessToken');
  
  if (!isLoggedIn) {
      return `
          <div class="review-login-prompt card p-4 text-center">
              <i class="fas fa-lock fa-2x text-muted mb-3"></i>
              <h5>Đăng nhập để đánh giá</h5>
              <p class="text-muted mb-3">Bạn cần đăng nhập để có thể viết đánh giá</p>
              <button class="btn btn-primary" onclick="redirectToLogin()">
                  <i class="fas fa-sign-in-alt me-2"></i>Đăng nhập ngay
              </button>
          </div>
      `;
  }

  return `
      <div class="review-form card p-4">
          <h5 class="card-title mb-4">Viết đánh giá của bạn</h5>
          <form id="reviewForm" onsubmit="submitReview(event, '${productId}')">
              <div class="rating-input mb-3 text-center">
                  <div class="rating-stars fs-3">
                      ${Array(5).fill('').map((_, i) => `
                          <i class="far fa-star rating-star" 
                             data-rating="${i + 1}"
                             onmouseover="highlightStars(${i + 1})"
                             onmouseout="resetStars()"
                             onclick="setRating(${i + 1})">
                          </i>
                      `).join('')}
                  </div>
                  <input type="hidden" name="rating" id="ratingInput" required>
              </div>

              <div class="mb-3">
                  <input type="text" 
                         class="form-control" 
                         name="title" 
                         placeholder="Tiêu đề đánh giá (không bắt buộc)">
              </div>

              <div class="mb-3">
                  <textarea class="form-control" 
                            name="comment" 
                            rows="4" 
                            placeholder="Chia sẻ trải nghiệm của bạn về sản phẩm..."
                            required>
                  </textarea>
              </div>

              <div class="mb-3">
                  <label class="form-label">Thêm hình ảnh (không bắt buộc)</label>
                  <input type="file" 
                         class="form-control" 
                         name="images" 
                         multiple 
                         accept="image/*">
              </div>

              <button type="submit" class="btn btn-primary">
                  <i class="fas fa-paper-plane me-2"></i>Gửi đánh giá
              </button>
          </form>
      </div>
  `;
}
// 10. Cart Functions
const CartManager = {
  async addToCart(productId, quantity) {
      const userId = localStorage.getItem('userId');
      const accessToken = localStorage.getItem('accessToken');

      if (!userId || !accessToken) {
          Swal.fire({
              icon: 'error',
              title: 'Lỗi',
              text: 'Bạn cần đăng nhập để thêm vào giỏ hàng'
          });
          return;
      }

      try {
          const response = await fetch(`${CONFIG.API.CART_URL}/cart/add-item/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${accessToken}`
              },
              body: JSON.stringify({
                  user_id: userId,
                  product_id: productId,
                  quantity: quantity
              })
          });

          const data = await response.json();

          if (!response.ok) {
              throw new Error(data.detail || "Không thể thêm vào giỏ hàng");
          }

          // Show success notification
          Swal.fire({
              icon: 'success',
              title: 'Thành công!',
              text: 'Đã thêm sản phẩm vào giỏ hàng',
              timer: 1500
          });

          // Update cart count using global function
          window.updateCartCount();

          return data;
      } catch (error) {
          console.error("Lỗi:", error);
          Swal.fire({
              icon: 'error',
              title: 'Lỗi',
              text: error.message
          });
      }
  }
};

// Update setupAddToCartButton function
function setupAddToCartButton(product) {
  const addToCartBtn = document.querySelector('.add-to-cart');
  if (!addToCartBtn) return;

  addToCartBtn.addEventListener('click', async () => {
      if (!localStorage.getItem('accessToken')) {
          redirectToLogin();
          return;
      }

      const quantity = parseInt(document.getElementById('quantity-input').value);
      await CartManager.addToCart(product._id, quantity);
  });
}

// Update setupBuyNowButton function
function setupBuyNowButton(product) {
  const buyNowBtn = document.querySelector('.buy-now');
  if (!buyNowBtn) return;

  buyNowBtn.addEventListener('click', async () => {
      if (!localStorage.getItem('accessToken')) {
          redirectToLogin();
          return;
      }

      const quantity = parseInt(document.getElementById('quantity-input').value);
      const result = await CartManager.addToCart(product._id, quantity);
      if (result) {
          window.location.href = '/checkout';
      }
  });
}

// Remove the old toast notifications since we're using SweetAlert2
// Remove these functions:
// - showSuccessMessage
// - showErrorMessage
// - updateCartBadge

// 11. Event Handlers
function setupProductInteractions(product) {
  setupQuantityControls();
  setupAddToCartButton(product);
  setupBuyNowButton(product);
  setupImageGallery();
  setupRatingStars();
}

function setupQuantityControls() {
  const minusBtn = document.getElementById('minus-btn');
  const plusBtn = document.getElementById('plus-btn');
  const quantityInput = document.getElementById('quantity-input');

  if (!minusBtn || !plusBtn || !quantityInput) return;

  minusBtn.addEventListener('click', () => {
      const currentValue = parseInt(quantityInput.value);
      if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
      }
  });

  plusBtn.addEventListener('click', () => {
      const currentValue = parseInt(quantityInput.value);
      const maxValue = parseInt(quantityInput.max);
      if (currentValue < maxValue) {
          quantityInput.value = currentValue + 1;
      }
  });

  quantityInput.addEventListener('change', () => {
      let value = parseInt(quantityInput.value);
      const maxValue = parseInt(quantityInput.max);
      
      if (isNaN(value) || value < 1) value = 1;
      if (value > maxValue) value = maxValue;
      
      quantityInput.value = value;
  });
}

function setupAddToCartButton(product) {
  const addToCartBtn = document.querySelector('.add-to-cart');
  if (!addToCartBtn) return;

  addToCartBtn.addEventListener('click', async () => {
      if (!localStorage.getItem('accessToken')) {
          redirectToLogin();
          return;
      }

      const quantity = parseInt(document.getElementById('quantity-input').value);
      await CartManager.addToCart(product._id, quantity);
  });
}

function setupBuyNowButton(product) {
  const buyNowBtn = document.querySelector('.buy-now');
  if (!buyNowBtn) return;

  buyNowBtn.addEventListener('click', async () => {
      if (!localStorage.getItem('accessToken')) {
          redirectToLogin();
          return;
      }

      const quantity = parseInt(document.getElementById('quantity-input').value);
      await CartManager.addToCart(product._id, quantity);
      window.location.href = '/checkout';
  });
}

function setupImageGallery() {
  const thumbnails = document.querySelectorAll('.thumbnail-wrapper');
  thumbnails.forEach(thumb => {
      thumb.addEventListener('click', () => {
          const fullImage = thumb.querySelector('img').dataset.full;
          const mainImage = document.querySelector('.main-product-image');
          mainImage.src = fullImage;
      });
  });
}

function setupRatingStars() {
  const stars = document.querySelectorAll('.rating-star');
  const ratingInput = document.getElementById('ratingInput');
  if (!stars.length || !ratingInput) return;

  stars.forEach(star => {
      star.addEventListener('mouseover', () => {
          const rating = parseInt(star.dataset.rating);
          highlightStars(rating);
      });

      star.addEventListener('mouseout', () => {
          const currentRating = parseInt(ratingInput.value) || 0;
          highlightStars(currentRating);
      });

      star.addEventListener('click', () => {
          const rating = parseInt(star.dataset.rating);
          ratingInput.value = rating;
          highlightStars(rating);
      });
  });
}

function highlightStars(rating) {
  const stars = document.querySelectorAll('.rating-star');
  stars.forEach((star, index) => {
      star.classList.toggle('fas', index < rating);
      star.classList.toggle('far', index >= rating);
      star.classList.toggle('text-warning', index < rating);
  });
}

function redirectToLogin() {
  const currentPath = encodeURIComponent(window.location.pathname + window.location.search);
  window.location.href = `/login?redirect=${currentPath}`;
}

// 12. Image Gallery Functions
const ImageGallery = {
  init() {
      this.setupZoom();
      this.setupLightbox();
      this.setupThumbnailControls();
  },

  setupZoom() {
      const mainImage = document.querySelector('.main-product-image');
      if (!mainImage) return;

      mainImage.addEventListener('mousemove', (e) => {
          const { left, top, width, height } = mainImage.getBoundingClientRect();
          const x = (e.clientX - left) / width * 100;
          const y = (e.clientY - top) / height * 100;
          
          mainImage.style.transformOrigin = `${x}% ${y}%`;
      });

      mainImage.addEventListener('mouseenter', () => {
          mainImage.style.transform = 'scale(1.5)';
      });

      mainImage.addEventListener('mouseleave', () => {
          mainImage.style.transform = 'scale(1)';
          mainImage.style.transformOrigin = 'center center';
      });
  },

  setupLightbox() {
      const lightboxTemplate = `
          <div class="product-lightbox" id="productLightbox">
              <div class="lightbox-overlay"></div>
              <div class="lightbox-content">
                  <button class="lightbox-close">&times;</button>
                  <button class="lightbox-prev"><i class="fas fa-chevron-left"></i></button>
                  <button class="lightbox-next"><i class="fas fa-chevron-right"></i></button>
                  <div class="lightbox-image-container">
                      <img src="" alt="Product image" class="lightbox-image">
                  </div>
                  <div class="lightbox-thumbnails"></div>
              </div>
          </div>
      `;
      document.body.insertAdjacentHTML('beforeend', lightboxTemplate);
      
      this.setupLightboxEvents();
  },

  setupLightboxEvents() {
      const lightbox = document.getElementById('productLightbox');
      const mainImage = document.querySelector('.main-product-image');
      const thumbnails = document.querySelectorAll('.thumbnail-image');
      
      // Open lightbox on main image click
      mainImage?.addEventListener('click', () => {
          this.openLightbox(mainImage.src);
      });

      // Open lightbox on thumbnail click
      thumbnails.forEach(thumb => {
          thumb.addEventListener('click', (e) => {
              e.preventDefault();
              this.openLightbox(thumb.dataset.full);
          });
      });

      // Close lightbox events
      lightbox?.querySelector('.lightbox-close')?.addEventListener('click', () => {
          this.closeLightbox();
      });

      lightbox?.querySelector('.lightbox-overlay')?.addEventListener('click', () => {
          this.closeLightbox();
      });
  },

  openLightbox(imageSrc) {
      const lightbox = document.getElementById('productLightbox');
      const lightboxImage = lightbox.querySelector('.lightbox-image');
      
      lightboxImage.src = imageSrc;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';

      // Update thumbnails
      this.updateLightboxThumbnails(imageSrc);
  },

  closeLightbox() {
      const lightbox = document.getElementById('productLightbox');
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
  },

  updateLightboxThumbnails(currentSrc) {
      const thumbnailContainer = document.querySelector('.lightbox-thumbnails');
      const allImages = [
          document.querySelector('.main-product-image').src,
          ...Array.from(document.querySelectorAll('.thumbnail-image')).map(img => img.dataset.full)
      ];

      thumbnailContainer.innerHTML = allImages
          .filter((src, index, array) => array.indexOf(src) === index)
          .map(src => `
              <div class="lightbox-thumbnail ${src === currentSrc ? 'active' : ''}" 
                   onclick="ImageGallery.switchLightboxImage('${src}')">
                  <img src="${src}" alt="Thumbnail">
              </div>
          `).join('');
  },

  switchLightboxImage(src) {
      const lightboxImage = document.querySelector('.lightbox-image');
      lightboxImage.src = src;
      this.updateLightboxThumbnails(src);
  }
};

// Initialize gallery when document is ready
document.addEventListener('DOMContentLoaded', () => {
  ImageGallery.init();
});

